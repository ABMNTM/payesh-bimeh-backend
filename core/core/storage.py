from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STATIC_BUCKET_NAME
    endpoint_url = settings.AWS_S3_STORAGE_URL
    querystring_auth = False
    default_acl = "public-read"


class MediaStorage(S3Boto3Storage):
    default_acl = "private"
    endpoint_url = settings.AWS_S3_STORAGE_URL
    file_overwrite = False
