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
    return kwargs


class EmailHostsBackend(EmailBackend):
    def send_messages(self, email_messages):
        if default := self.default_from_email:
            for message in email_messages:
                if message.from_email == settings.DEFAULT_FROM_EMAIL:
                    message.from_email = default
        return super().send_messages(email_messages)


def get_connection(key):
    if dsn := settings.EMAIL_HOSTS.get(key):
        config = dj_email_url.parse(dsn)
        backend = EmailHostsBackend(**parse_conf(config))
        backend.default_from_email = config.get("DEFAULT_FROM_EMAIL", "")
        return backend
    return _orig_get_connection()
