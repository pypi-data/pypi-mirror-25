from django.conf import settings as system_settings
from .settings import auth_settings

_app_lable = auth_settings.REMOTE_AUTH_APP

if '%s.backends.CustomModelBackend' % _app_lable not in system_settings.AUTHENTICATION_BACKENDS:
    system_settings.AUTHENTICATION_BACKENDS.append('%s.backends.CustomModelBackend' % _app_lable)