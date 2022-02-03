==============================================================================
django-email-hosts -- Support for several SMTP configurations in a single site
==============================================================================

.. image:: https://github.com/feinheit/django-email-hosts/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/feinheit/django-email-hosts/
    :alt: CI Status


Why?
====

Some projects may want to sent emails over multiple SMTP relays or smarthosts.
Examples are sites running on multiple domains, e.g. ``info@example.com`` and
``info@example.org``. It may be possible to use the same SMTP credentials for
each sender address but if that isn't possible django-email-hosts may be a good
solution for the problem.


Usage
=====

- **Install**: ``pip install django-email-hosts``
- **Configure**: Add the ``EMAIL_HOSTS`` setting
- **Use**: Always explicitly use the SMTP connection returned by
  ``email_hosts.backends.get_connection``


``EMAIL_HOSTS``
===============

django-email-hosts uses the excellent `dj-email-url
<https://github.com/migonzalvar/dj-email-url>`__ library under the hood. Each
SMTP connection is configured using a dj-email-url DSN.

The keys of the ``EMAIL_HOSTS`` dictionary are defined by you and there's no
deeper meaning to them.

An example configuration (which is possibly nonsensical) looks like this:


.. code-block:: python

    EMAIL_HOSTS = {
        "sendgrid": "submission://USER:PASSWORD@smtp.sendgrid.com?_default_from_email=info@example.com",
        "mailgun": "submission://USER:PASSWORD@smtp.mailgun.com?_default_from_email=info@example.org",
    }

This configuration creates two SMTP backends, one using sendgrid and one using
mailgun. The ``_default_from_email`` is completely optional. If the email
message's ``from_email`` isn't set (resp. is equal to the
``DEFAULT_FROM_EMAIL`` setting) it automatically defaults to the per-backend
value.


``email_hosts.backends.get_connection``
=======================================

The ``get_connection`` function expects a single key for the ``EMAIL_HOSTS``
setting above. Sending a single email using an explicit connection may look as
follows, using the settings from above:

.. code-block:: python

    from django.core.mail import EmailMessage
    from email_hosts.backends import get_connection

    EmailMessage(
        "Hello",
        "World",
        to=["recipient@example.com"],
        connection=use_backend("sendgrid"),
    ).send()

``get_connection`` currently silently returns the default email backend if the
key doesn't exist in the ``EMAIL_HOSTS`` dictionary.
