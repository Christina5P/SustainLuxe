from django.conf import settings
from storages.backends.sboto3 import S3BotoStorage


class StaticStorage(S3Boto3Storage):
    locations = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    locations = settings.MEDIAFILES_LOCATION
