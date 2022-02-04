import dj_email_url
from django.conf import settings
from django.core.mail import get_connection as _orig_get_connection
from django.core.mail.backends.smtp import EmailBackend


__all__ = ["get_connection"]


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
    def _send(self, email_message):
        if (
            self.default_from_email
            and email_message.from_email == settings.DEFAULT_FROM_EMAIL
        ):
            email_message.from_email = self.default_from_email
        return super()._send(email_message)


def get_connection(key):
    if dsn := settings.EMAIL_HOSTS.get(key):
        config = dj_email_url.parse(dsn)
        backend = EmailHostsBackend(**parse_conf(config))
        backend.default_from_email = config.get("DEFAULT_FROM_EMAIL", "")
        return backend
    return _orig_get_connection()
