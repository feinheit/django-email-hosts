from functools import cache

import dj_email_url
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import get_connection
from django.core.mail.backends.smtp import EmailBackend


DEFAULT_CONF = "EMAIL_HOSTS"


def parse_conf(
    EMAIL_HOST=None,
    EMAIL_PORT=None,
    EMAIL_FILE_PATH=None,
    EMAIL_HOST_USER=None,
    EMAIL_HOST_PASSWORD=None,
    EMAIL_USE_TLS=None,
    EMAIL_USE_SSL=None,
    EMAIL_BACKEND=None,
    EMAIL_SSL_KEYFILE=None,
    EMAIL_SSL_CERTFILE=None,
    SERVER_EMAIL=None,
    DEFAULT_FROM_EMAIL=None,
):
    return {
        "host": EMAIL_HOST,
        "port": EMAIL_PORT,
        "username": EMAIL_HOST_USER,
        "password": EMAIL_HOST_PASSWORD,
        "use_tls": EMAIL_USE_TLS,
        "use_ssl": EMAIL_USE_SSL,
        "ssl_keyfile": EMAIL_SSL_KEYFILE,
        "ssl_certfile": EMAIL_SSL_CERTFILE,
    }


class EmailBackendProvider:
    def __init__(self):
        hosts_config = getattr(settings, DEFAULT_CONF)
        self.fallback = get_connection()

        self.backends = (
            {
                k: EmailBackend(**parse_conf(**dj_email_url.parse(url)))
                for k, url in hosts_config.items()
            }
            if hosts_config
            else None
        )

    def get_backend(self, key):
        if self.backends and key in self.backends:
            return self.backends[key]
        elif self.fallback:
            return self.fallback
        else:
            raise ImproperlyConfigured(
                "Email backend for key '%s' and fallback not configured." % (key)
            )


@cache
def _provider():
    return EmailBackendProvider()


def use_backend(key):
    return _provider().get_backend(key)
