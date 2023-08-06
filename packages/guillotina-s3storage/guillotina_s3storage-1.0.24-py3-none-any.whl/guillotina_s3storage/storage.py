# -*- coding: utf-8 -*-

from aiohttp.web import StreamResponse
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzlocal
from guillotina import app_settings
from guillotina import configure
from guillotina.browser import Response
from guillotina.component import getUtility
from guillotina.event import notify
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IApplication
from guillotina.interfaces import IFileManager
from guillotina.interfaces import IRequest
from guillotina.interfaces import IResource
from guillotina.interfaces import IValueToJson
from guillotina.schema import Object
from guillotina.schema.fieldproperty import FieldProperty
from guillotina.utils import get_content_path
from guillotina.utils import get_current_request
from guillotina_s3storage.events import FinishS3Upload
from guillotina_s3storage.events import InitialS3Upload
from guillotina_s3storage.interfaces import IS3BlobStore
from guillotina_s3storage.interfaces import IS3File
from guillotina_s3storage.interfaces import IS3FileField
from guillotina_s3storage.utils import aretriable
from io import BytesIO
from zope.interface import implementer

import aiobotocore
import asyncio
import base64
import boto3
import botocore
import logging
import mimetypes
import uuid


log = logging.getLogger('pserver.storage')

MAX_SIZE = 1073741824

MIN_UPLOAD_SIZE = 5 * 1024 * 1024
CHUNK_SIZE = MIN_UPLOAD_SIZE
MAX_REQUEST_CACHE_SIZE = 6 * 1024 * 1024
MAX_RETRIES = 5


class UnRetryableRequestError(Exception):
    pass


async def read_request_data(request, chunk_size=CHUNK_SIZE):
    if getattr(request, '_retry_attempt', 0) > 0:
        # we are on a retry request, see if we have read cached data yet...
        if request._retry_attempt > getattr(request, '_last_cache_data_retry_count', 0):
            if request._cache_data is None:
                # request payload was too large to fit into request cache.
                # so retrying this request is not supported and we need to throw
                # another error
                raise UnRetryableRequestError()
            data = request._cache_data[request._last_read_pos:request._last_read_pos + chunk_size]
            request._last_read_pos += len(data)
            if request._last_read_pos >= len(request._cache_data):
                # done reading cache data
                request._last_cache_data_retry_count = request._retry_attempt
            return data

    if not hasattr(request, '_cache_data'):
        request._cache_data = b''

    try:
        data = await request.content.readexactly(chunk_size)
    except asyncio.IncompleteReadError as e:
        data = e.partial

    if request._cache_data is not None:
        if len(request._cache_data) + len(data) > MAX_REQUEST_CACHE_SIZE:
            # we only allow caching up to chunk size, otherwise, no cache data..
            request._cache_data = None
        else:
            request._cache_data += data

    request._last_read_pos += len(data)
    return data


class S3Exception(Exception):
    pass


def _to_str(value):
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    return value


@configure.adapter(
    for_=IS3File,
    provides=IValueToJson)
def json_converter(value):
    if value is None:
        return value
    return {
        'filename': value.filename,
        'content_type': _to_str(value.content_type),
        'size': value.size,
        'extension': value.extension,
        'md5': value.md5
    }


@configure.adapter(
    for_=(IResource, IRequest, IS3FileField),
    provides=IFileManager)
class S3FileManager(object):

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    async def upload(self):
        """In order to support TUS and IO upload.

        we need to provide an upload that concats the incoming
        """
        self.context._p_register()  # writing to object

        file = self.field.get(self.context)
        if file is None:
            file = S3File(content_type=self.request.content_type)
            self.field.set(self.context, file)
            # XXX no savepoint support right now?
            # trns = get_transaction(self.request)
            # trns.savepoint()
        if 'X-UPLOAD-MD5HASH' in self.request.headers:
            file._md5 = self.request.headers['X-UPLOAD-MD5HASH']
        else:
            file._md5 = None

        if 'X-UPLOAD-EXTENSION' in self.request.headers:
            file._extension = self.request.headers['X-UPLOAD-EXTENSION']
        else:
            file._extension = None

        if 'X-UPLOAD-SIZE' in self.request.headers:
            file._size = int(self.request.headers['X-UPLOAD-SIZE'])
        else:
            raise AttributeError('x-upload-size header needed')

        if 'X-UPLOAD-FILENAME' in self.request.headers:
            file.filename = self.request.headers['X-UPLOAD-FILENAME']
        elif 'X-UPLOAD-FILENAME-B64' in self.request.headers:
            file.filename = base64.b64decode(
                self.request.headers['X-UPLOAD-FILENAME-B64']).decode("utf-8")
        else:
            file.filename = uuid.uuid4().hex

        await file.initUpload(self.context)
        self.request._last_read_pos = 0
        data = await read_request_data(self.request)

        count = 0

        # If we have data or is an empty file
        while data or (len(data) == 0 and count == 0):
            old_current_upload = file._current_upload  # noqa
            await file.appendData(data)
            count += 1
            data = await read_request_data(self.request)

        # Test resp and checksum to finish upload
        await file.finishUpload(self.context)

    async def tus_create(self):
        self.context._p_register()  # writing to object

        # This only happens in tus-java-client, redirect this POST to a PATCH
        if self.request.headers.get('X-HTTP-Method-Override') == 'PATCH':
            return await self.tus_patch()

        file = self.field.get(self.context)
        if file is None:
            file = S3File(content_type=self.request.content_type)
            self.field.set(self.context, file)
        if 'CONTENT-LENGTH' in self.request.headers:
            file._current_upload = int(self.request.headers['CONTENT-LENGTH'])
        else:
            file._current_upload = 0

        if 'UPLOAD-LENGTH' in self.request.headers:
            file._size = int(self.request.headers['UPLOAD-LENGTH'])
        else:
            raise AttributeError('We need upload-length header')

        if 'UPLOAD-MD5' in self.request.headers:
            file._md5 = self.request.headers['UPLOAD-MD5']

        if 'UPLOAD-EXTENSION' in self.request.headers:
            file._extension = self.request.headers['UPLOAD-EXTENSION']

        if 'TUS-RESUMABLE' not in self.request.headers:
            raise AttributeError('Its a TUS needs a TUS version')

        if 'UPLOAD-FILENAME' in self.request.headers:
            file.filename = self.request.headers['UPLOAD-FILENAME']
        elif 'UPLOAD-METADATA' not in self.request.headers:
            file.filename = uuid.uuid4().hex
        else:
            filename = self.request.headers['UPLOAD-METADATA']
            file.filename = base64.b64decode(filename.split()[1]).decode('utf-8')

        if file.size < MIN_UPLOAD_SIZE:
            file._one_tus_shoot = True
        else:
            file._one_tus_shoot = False

        await file.initUpload(self.context)

        # Location will need to be adapted on aiohttp 1.1.x
        resp = Response(headers={
            'Location': IAbsoluteURL(
                self.context, self.request)() + '/@tusupload/' + self.field.__name__,
            'Tus-Resumable': '1.0.0',
            'Access-Control-Expose-Headers': 'Location,Tus-Resumable'
        }, status=201)
        return resp

    async def tus_patch(self):
        self.context._p_register()  # writing to object

        file = self.field.get(self.context)
        if 'CONTENT-LENGTH' in self.request.headers:
            to_upload = int(self.request.headers['CONTENT-LENGTH'])
        else:
            raise AttributeError('No content-length header')

        if 'UPLOAD-OFFSET' in self.request.headers:
            file._current_upload = int(self.request.headers['UPLOAD-OFFSET'])
        else:
            raise AttributeError('No upload-offset header')

        self.request._last_read_pos = 0
        data = await read_request_data(self.request, to_upload)

        if file.one_tus_shoot:
            # One time shoot
            if file._block > 1:
                raise AttributeError('You should push 5Mb blocks AWS')
            await file.oneShotUpload(self.context, data)
            expiration = datetime.now() + timedelta(days=365)
        else:
            count = 0
            while data:
                resp = await file.appendData(data)
                count += 1

                data = await read_request_data(self.request)

            expiration = file._resumable_uri_date + timedelta(days=7)
        if file._size <= file._current_upload:
            await file.finishUpload(self.context)
        resp = Response(headers={
            'Upload-Offset': str(file.actualSize()),
            'Tus-Resumable': '1.0.0',
            'Upload-Expires': expiration.isoformat(),
            'Access-Control-Expose-Headers': 'Upload-Offset,Upload-Expires,Tus-Resumable'
        })
        return resp

    async def tus_head(self):
        file = self.field.get(self.context)
        if file is None:
            raise KeyError('No file on this context')
        head_response = {
            'Upload-Offset': str(file.actualSize()),
            'Tus-Resumable': '1.0.0',
            'Access-Control-Expose-Headers': 'Upload-Offset,Upload-Length,Tus-Resumable'
        }
        if file.size:
            head_response['Upload-Length'] = str(file._size)
        resp = Response(headers=head_response)
        return resp

    async def tus_options(self):
        resp = Response(headers={
            'Tus-Resumable': '1.0.0',
            'Tus-Version': '1.0.0',
            'Tus-Max-Size': '1073741824',
            'Tus-Extension': 'creation,expiration'
        })
        return resp

    async def download(self, disposition=None):
        if disposition is None:
            disposition = self.request.GET.get('disposition', 'attachment')
        file = self.field.get(self.context)
        if file is None:
            raise AttributeError('No field value')

        cors_renderer = app_settings['cors_renderer'](self.request)
        headers = await cors_renderer.get_headers()
        headers.update({
            'CONTENT-DISPOSITION': f'{disposition}; filename="%s"' % file.filename
        })

        resp = StreamResponse(headers=headers)
        resp.content_type = file.guess_content_type()
        resp.content_length = file._size

        downloader = await file.download(None)
        await resp.prepare(self.request)

        async with downloader['Body'] as stream:
            data = await stream.read(CHUNK_SIZE)

            while data:
                resp.write(data)
                data = await stream.read(CHUNK_SIZE)

        return resp

    async def iter_data(self):
        file = self.field.get(self.context)
        if file is None:
            raise AttributeError('No field value')

        downloader = await file.download(None)

        async with downloader['Body'] as stream:
            data = await stream.read(CHUNK_SIZE)
            while True:
                if not data:
                    break
                yield data
                data = await stream.read(CHUNK_SIZE)

    async def save_file(self, generator, content_type=None, size=None,
                        filename=None):
        self.context._p_register()  # writing to object

        file = self.field.get(self.context)
        if file is None:
            file = S3File(content_type=content_type)
            self.field.set(self.context, file)

        file._size = size
        if filename is None:
            filename = uuid.uuid4().hex
        file.filename = filename

        await file.initUpload(self.context)

        async for data in generator():
            await file.appendData(data)

        await file.finishUpload(self.context)


@implementer(IS3File)
class S3File:
    """File stored in a GCloud, with a filename."""

    filename = FieldProperty(IS3File['filename'])

    def __init__(self, content_type='application/octet-stream',
                 filename=None, size=0, md5=None):
        if not isinstance(content_type, bytes):
            content_type = content_type.encode('utf8')
        self.content_type = content_type
        if filename is not None:
            self.filename = filename
            extension_discovery = filename.split('.')
            if len(extension_discovery) > 1:
                self._extension = extension_discovery[-1]
        elif self.filename is None:
            self.filename = uuid.uuid4().hex

        self._size = size
        self._md5 = md5

    def guess_content_type(self):
        ct = _to_str(self.content_type)
        if ct == 'application/octet-stream':
            # try guessing content_type
            ct, _ = mimetypes.guess_type(self.filename)
            if ct is None:
                ct = 'application/octet-stream'
        return ct

    def generate_key(self, request, context):
        return '{}{}/{}::{}'.format(
            request._container_id,
            get_content_path(context),
            context._p_oid,
            uuid.uuid4().hex)

    async def copy_cloud_file(self, new_uri):
        if self.uri is None:
            Exception('To rename a uri must be set on the object')
        util = getUtility(IS3BlobStore)

        await util._s3aioclient.copy_object(
            CopySource={'Bucket': self._bucket_name, 'Key': self.uri},
            Bucket=self._bucket_name, Key=new_uri)
        old_uri = self.uri
        self._uri = new_uri
        return old_uri

    async def rename_cloud_file(self, new_uri):
        old_uri = await self.copy_cloud_file(new_uri)
        util = getUtility(IS3BlobStore)
        await util._s3aioclient.delete_object(
            Bucket=self._bucket_name, Key=old_uri)

    async def initUpload(self, context):
        """Init an upload.

        self._uload_file_id : temporal url to image beeing uploaded
        self._resumable_uri : uri to resumable upload
        self._uri : finished uploaded image
        """
        util = getUtility(IS3BlobStore)
        request = get_current_request()
        if hasattr(self, '_upload_file_id') and self._upload_file_id is not None:  # noqa
            if getattr(self, '_mpu', None) is not None:
                await self._abort_multipart()
            self._mpu = None
            self._upload_file_id = None

        bucket_name = await util.get_bucket_name()
        self._bucket_name = bucket_name
        self._upload_file_id = self.generate_key(request, context)
        self._multipart = {'Parts': []}
        if not self.one_tus_shoot:
            await self._create_multipart()
        self._current_upload = 0
        self._block = 1
        self._resumable_uri_date = datetime.now(tz=tzlocal())
        await notify(InitialS3Upload(context))

    @aretriable(3)
    async def _create_multipart(self):
        util = getUtility(IS3BlobStore)
        self._mpu = await util._s3aioclient.create_multipart_upload(
            Bucket=self._bucket_name, Key=self._upload_file_id)

    @aretriable(3)
    async def _abort_multipart(self):
        util = getUtility(IS3BlobStore)
        await util._s3aioclient.abort_multipart_upload(
            Bucket=self._bucket_name,
            Key=self._upload_file_id,
            UploadId=self._mpu['UploadId'])

    async def appendData(self, data):
        part = await self._upload_part(data)
        self._multipart['Parts'].append({
            'PartNumber': self._block,
            'ETag': part['ETag']
        })
        self._current_upload += len(data)
        self._block += 1
        return part

    @aretriable(3)
    async def _upload_part(self, data):
        util = getUtility(IS3BlobStore)
        return await util._s3aioclient.upload_part(
            Bucket=self._bucket_name,
            Key=self._upload_file_id,
            PartNumber=self._block,
            UploadId=self._mpu['UploadId'],
            Body=data)

    def actualSize(self):
        return self._current_upload

    async def finishUpload(self, context):
        util = getUtility(IS3BlobStore)
        # It would be great to do on AfterCommit
        if self.uri is not None:
            try:
                await util._s3aioclient.delete_object(
                    Bucket=self._bucket_name, Key=self.uri)
            except botocore.exceptions.ClientError as e:
                log.warn('Error deleting object', exc_info=True)
        self._uri = self._upload_file_id
        if self._mpu is not None:
            await self._complete_multipart_upload()
        self._multipart = None
        self._block = None
        self._upload_file_id = None
        await notify(FinishS3Upload(context))

    @aretriable(3)
    async def _complete_multipart_upload(self):
        util = getUtility(IS3BlobStore)
        await util._s3aioclient.complete_multipart_upload(
            Bucket=self._bucket_name,
            Key=self._upload_file_id,
            UploadId=self._mpu['UploadId'],
            MultipartUpload=self._multipart)

    async def oneShotUpload(self, context, data):
        util = getUtility(IS3BlobStore)

        if hasattr(self, '_upload_file_id') and self._upload_file_id is not None:  # noqa
            if getattr(self, '_mpu', None) is not None:
                await util._s3aioclient.abort_multipart_upload(
                    Bucket=self._bucket_name,
                    Key=self._upload_file_id,
                    UploadId=self._mpu['UploadId'])
            self._mpu = None
            self._upload_file_id = None
        file_data = BytesIO(data)
        bucket_name = await util.get_bucket_name()
        self._bucket_name = bucket_name
        request = get_current_request()
        self._upload_file_id = request._container_id + '/' + uuid.uuid4().hex

        response = await self._upload_fileobj(file_data)

        self._block += 1
        self._current_upload += len(data)
        return response

    @aretriable(3)
    async def _upload_fileobj(self, file_data):
        util = getUtility(IS3BlobStore)
        # XXX no support for upload_fileobj in aiobotocore so run in executor
        root = getUtility(IApplication, name='root')
        response = await util._loop.run_in_executor(
            root.executor, util._s3client.upload_fileobj,
            file_data,
            self._bucket_name,
            self._upload_file_id)
        return response

    async def deleteUpload(self, uri=None):
        util = getUtility(IS3BlobStore)
        if uri is None:
            uri = self.uri
        if uri is not None:
            try:
                await util._s3aioclient.delete_object(
                    Bucket=self._bucket_name, Key=uri)
            except botocore.exceptions.ClientError as e:
                log.warn('Error deleting object', exc_info=True)
        else:
            raise AttributeError('No valid uri')

    async def download(self, buf):
        if not hasattr(self, '_uri'):
            url = self._upload_file_id
        else:
            url = self._uri

        return await self._download(url)

    @aretriable(3)
    async def _download(self, url):
        util = getUtility(IS3BlobStore)
        return await util._s3aioclient.get_object(Bucket=self._bucket_name, Key=url)

    def _set_data(self, data):
        raise NotImplemented('Only specific upload permitted')

    def _get_data(self):
        raise NotImplemented('Only specific download permitted')

    data = property(_get_data, _set_data)

    @property
    def uri(self):
        if hasattr(self, '_uri'):
            return self._uri

    @property
    def size(self):
        if hasattr(self, '_size'):
            return self._size
        else:
            return None

    @property
    def md5(self):
        if hasattr(self, '_md5'):
            return self._md5
        else:
            return None

    @property
    def extension(self):
        if hasattr(self, '_extension'):
            return self._extension
        else:
            return None

    @property
    def one_tus_shoot(self):
        if hasattr(self, '_one_tus_shoot'):
            return self._one_tus_shoot
        else:
            return False


@implementer(IS3FileField)
class S3FileField(Object):
    """A NamedBlobFile field."""

    _type = S3File
    schema = IS3File

    def __init__(self, **kw):
        if 'schema' in kw:
            self.schema = kw.pop('schema')
        super(S3FileField, self).__init__(schema=self.schema, **kw)


# Configuration Utility

class S3BlobStore(object):

    def __init__(self, settings, loop=None):
        self._aws_access_key = settings['aws_client_id']
        self._aws_secret_key = settings['aws_client_secret']

        opts = dict(
            aws_secret_access_key=self._aws_secret_key,
            aws_access_key_id=self._aws_access_key,
            endpoint_url=settings.get('endpoint_url'),
            verify=settings.get('verify_ssl'),
            use_ssl=settings.get('ssl', True),
            region_name=settings.get('region_name')
        )

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

        self._s3aiosession = aiobotocore.get_session(loop=loop)

        # This client is for downloads only
        self._s3aioclient = self._s3aiosession.create_client('s3', **opts)
        self._cached_buckets = []

        self._bucket_name = settings['bucket']

        # right now, only used for upload_fileobj in executor
        self._s3client = boto3.client('s3', **opts)

    async def get_bucket_name(self):
        request = get_current_request()
        bucket_name = request._container_id.lower() + '.' + self._bucket_name

        if bucket_name in self._cached_buckets:
            return bucket_name

        missing = False
        try:
            res = await self._s3aioclient.head_bucket(Bucket=bucket_name)
            if res['ResponseMetadata']['HTTPStatusCode'] == 404:
                missing = True
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                missing = True

        if missing:
            await self._s3aioclient.create_bucket(Bucket=bucket_name)
        return bucket_name

    async def initialize(self, app=None):
        # No asyncio loop to run
        self.app = app

    async def finalize(self, app=None):
        self._s3aiosession.close()

    async def iterate_bucket(self):
        req = get_current_request()
        bucket_name = await self.get_bucket_name()
        result = await self._s3aioclient.list_objects(
            Bucket=bucket_name, Prefix=req._container_id + '/')
        paginator = self._s3aioclient.get_paginator('list_objects')
        async for result in paginator.paginate(
                Bucket=bucket_name, Prefix=req._container_id + '/'):
            for item in result.get('Contents', []):
                yield item
