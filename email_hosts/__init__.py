import dj_email_url
from django.core.mail import get_connection
from django.core.mail.backends.smtp import EmailBackend
from django.core.exceptions import ImproperlyConfigured
from speckenv import env


DEFAULT_CONF = "EMAIL_HOSTS"


class EmailBackendProvider:
    def __init__(self, key=None):
        hosts_config = env(DEFAULT_CONF)
        self.fallback = get_connection()
        self.backends = (
            {
                k: EmailBackend(**dj_email_url.parse(url))
                for k, url in hosts_config.items()
            }
            if hosts_config
            else None
        )
        if key:
            return self.get_backend(key)

    def get_backend(self, key):
        if key in self.backends:
            return self.backends[key]
        elif self.fallback:
            return self.fallback
        else:
            raise ImproperlyConfigured(
                "Email backend for key '%s' and fallback not configured." % (key)
            )


BACKENDPROVIDER = EmailBackendProvider()


def use_backend(key):
    if hasattr(BACKENDPROVIDER, "get_backend"):
        return BACKENDPROVIDER.get_backend(key)
    else:
        return EmailBackendProvider(key)
