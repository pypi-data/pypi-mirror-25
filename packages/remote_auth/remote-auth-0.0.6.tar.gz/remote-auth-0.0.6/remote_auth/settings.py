from django.conf import settings


DEFAULTS = {
    'REMOTE_AUTH_APP': 'remote_auth',
}


class AuthSettings(object):

    def __init__(self, user_settings=None, defaults=None):
        self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS

    def __getattr__(self, attr):
        print(attr)
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self._user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


user_settings = getattr(settings, 'REMOTE_AUTH', {})

auth_settings = AuthSettings(user_settings, DEFAULTS)