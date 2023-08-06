from django.contrib.sessions.backends.db import SessionStore as SourceSessionStore
from .settings import auth_settings


class SessionStore(SourceSessionStore):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    @classmethod
    def get_model_class(cls):
        # Avoids a circular import and allows importing SessionStore when
        # django.contrib.sessions is not in INSTALLED_APPS.
        from .models import Session
        return Session

    def load(self):
        session_data = super(SessionStore, self).load()
        if '_auth_user_backend' in session_data:
            session_data['_auth_user_backend'] = '%s.backends.CustomModelBackend' % auth_settings.REMOTE_AUTH_APP
        print("session_data", session_data)
        return session_data
