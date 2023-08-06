from os import getenv

from django.conf import settings


def _get_value(django_key, env_key, default_value):
    if hasattr(settings, django_key):
        return getattr(settings, django_key)
    return getenv(env_key, default_value)


_default_bucket = 'plenario-exports'

_default_acl = 'public-read'

_default_email = 'plenario@lists.uchicago.edu'


S3_BUCKET = _get_value(
    'PLENARIO_EXPORT_S3_BUCKET',
    'PLENARIO_EXPORT_S3_BUCKET',
    _default_bucket)

S3_OBJECT_ACL = _get_value(
    'PLENARIO_EXPORT_S3_ACL',
    'PLENARIO_EXPORT_S3_ACL',
    _default_acl)

EMAIL_SENDER_ADDRESS = _get_value(
    'PLENARIO_EMAIL_SENDER_ADDRESS',
    'PLENARIO_EMAIL_SENDER_ADDRESS',
    _default_email)
