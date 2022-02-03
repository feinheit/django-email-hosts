from functools import cache

import dj_email_url
from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.backends.smtp import EmailBackend


def parse_conf(settings):
    kwargs = {
        "host": settings["EMAIL_HOST"],
        "port": settings["EMAIL_PORT"],
        "username": settings["EMAIL_HOST_USER"],
        "password": settings["EMAIL_HOST_PASSWORD"],
        "use_tls": settings["EMAIL_USE_TLS"],
        "use_ssl": settings["EMAIL_USE_SSL"],
    }
    if timeout := settings.get("EMAIL_TIMEOUT"):
        kwargs["timeout"] = timeout
    if ssl_keyfile := settings.get("EMAIL_SSL_KEYFILE"):
        kwargs["ssl_keyfile"] = ssl_keyfile
    if ssl_certfile := settings.get("EMAIL_SSL_CERTFILE"):
        kwargs["ssl_certfile"] = ssl_certfile
    return kwargs


class EmailHostsBackend(EmailBackend):
    @classmethod
    def from_dsn(cls, dsn):
        kwargs = parse_conf(dj_email_url.parse(dsn))
        default_from_email = kwargs.pop("DEFAULT_FROM_EMAIL", "")
        backend = cls(**kwargs)
        backend.default_from_email = default_from_email
        return backend


@cache
def use_backend(key):
    if dsn := settings.EMAIL_HOSTS.get(key):
        return EmailHostsBackend.from_dsn(dsn)
    return get_connection()
