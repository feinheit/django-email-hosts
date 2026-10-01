from speckenv_django import django_mailer_url


__version__ = "0.2.1"


def mailers(email_hosts, /):
    """
    Convert an ``EMAIL_HOSTS`` dictionary into ``MAILERS`` entries (Django 6.1+)
    """
    return {
        key: django_mailer_url(dsn, backend="email_hosts.backends.EmailHostsBackend")
        for key, dsn in email_hosts.items()
    }
