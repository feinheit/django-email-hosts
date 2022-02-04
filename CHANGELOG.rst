Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

- Removed the ``functools.cache`` decorator from ``get_connection`` --
  constructing backends isn't that expensive and the danger of memory leaks
  when misusing the connection management is worse.
- Removed support for the ``ssl_keyfile`` and ``ssl_certfile`` parameters since
  they are never returned by ``dj-email-url`` anyway.


`0.1`_ (2022-02-03)
~~~~~~~~~~~~~~~~~~~

- Initial release!

.. _0.1: https://github.com/feinheit/django-email-hosts/commit/747611e7285df
.. _Next version: https://github.com/feinheit/django-email-hosts/compare/0.1...main
