import boto3

from dashops.common.errors import CliRuntimeError

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class S3Service:
    @classmethod
    def list_bucket(cls, region_name=None):
        """
        Get the list of bucket names.
        :param region_name: region name to use.
        :return: a list of strings containing bucket names.
        """
        if region_name is None:
            region_name = 'us-west-1'
        s3 = boto3.resource('s3', region_name=region_name)
        return [bucket.name for bucket in s3.buckets.all()]

    @classmethod
    def create_bucket(cls, bucket_name, region_name=None, enable_version=True):
        """
        Create a bucket at specified region.
        :param bucket_name: the name of the bucket.
        :param region_name: the region to create.
        :param enable_version: if to enable versioning.
        :return: the bucket object.
        """
        if region_name is None:
            region_name = 'us-west-1'
        s3 = boto3.resource('s3', region_name=region_name)
        bucket = s3.Bucket(bucket_name)
        bucket.create(ACL='private', CreateBucketConfiguration={'LocationConstraint': region_name})
        if enable_version:
            bucket_versioning = bucket.Versioning()
            bucket_versioning.enable()
        return bucket

    @classmethod
    def download(cls, bucket_name, key, region_name=None, filename=None):
        """
        Download the given key from given bucket and return the content.
        If "filename" is specified, then download to the file and then return the content.
        :param bucket_name: name of the bucket to download from.
        :param key: object key on s3.
        :param region_name: region name to use.
        :param filename: if specified, download to the file.
        :return: content in the object.
        """
        if region_name is None:
            region_name = 'us-west-1'
        s3 = boto3.resource('s3', region_name=region_name)
        bucket = s3.Bucket(bucket_name)
        bucket.load()
        if filename:
            bucket.download_file(key, filename)
            with open(filename) as f:
                return f.read()
        else:
            s = BytesIO()
            bucket.download_fileobj(key, s)
            return s.getvalue().decode()

    @classmethod
    def upload(cls, bucket_name, key, content=None, region_name=None, filename=None):
        """
        Upload the given key to given bucket.
        If "filename" is specified, then upload the file.
        :param bucket_name: name of the bucket to upload to.
        :param key: object key on s3.
        :param content: content to upload to s3.
        :param region_name: region name to use.
        :param filename: if specified, upload the file.
        :return: None
        """
        if region_name is None:
            region_name = 'us-west-1'
        if bucket_name not in cls.list_bucket(region_name=region_name):
            raise CliRuntimeError('Please specify an existed bucket or create it first!')
        if content is None and filename is None:
            raise CliRuntimeError('Please specify one of "filename" or "content".')
        s3 = boto3.resource('s3', region_name=region_name)
        bucket = s3.Bucket(bucket_name)
        obj = bucket.Object(key)
        if filename:
            obj.upload_file(filename)
        else:
            s = BytesIO(content.encode('utf-8'))
            obj.upload_fileobj(s)
