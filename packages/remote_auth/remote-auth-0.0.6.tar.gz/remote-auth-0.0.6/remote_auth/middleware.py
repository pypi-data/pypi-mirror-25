from importlib import import_module

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from .session import SessionStore


class SessionMiddleware(SessionMiddleware):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.SessionStore = SessionStore

    def process_request(self, request):
        if request.session.load():
            return
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key)
