from django.apps import AppConfig
from .settings import auth_settings

class Remote_authConfig(AppConfig):
    name = auth_settings.REMOTE_AUTH_APP
