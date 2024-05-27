Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

.. _Next version: https://github.com/feinheit/django-email-hosts/compare/0.2...main

- Added Django 4.1, 4.2, 5.0, Python 3.11, 3.12.
- Fixed a typo in the README.
- Modernized the package.
- Added a command to send test mails using all configured email backends.


`0.2`_ (2022-02-07)
~~~~~~~~~~~~~~~~~~~

.. _0.2: https://github.com/feinheit/django-email-hosts/compare/0.1...0.2

- Removed the ``functools.cache`` decorator from ``get_connection`` --
  constructing backends isn't that expensive and the danger of memory leaks
  when misusing the connection management is worse.
- Removed support for the ``ssl_keyfile`` and ``ssl_certfile`` parameters since
  they are never returned by ``dj-email-url`` anyway.
- Changed the implementation to use documented APIs instead of undocumented
  internals of Django.
- Switched from ``dj-email-url`` to ``speckenv_django`` for parsing the email
  URL.


`0.1`_ (2022-02-03)
~~~~~~~~~~~~~~~~~~~

.. _0.1: https://github.com/feinheit/django-email-hosts/commit/747611e7285df

- Initial release!
