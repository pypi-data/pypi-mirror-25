pyramid\_crow
=============

.. image:: https://api.travis-ci.org/npilon/pyramid_crow.png?branch=master
        :target: https://travis-ci.org/npilon/pyramid_crow

``pyramid_crow`` provides a ``pyramid`` package for integrating with ``raven`` that is both automatic and complies with ``raven``'s ``http_context`` standard.

Usage
-----

1. Include ``pyramid_crow`` using either the ``pyramid.includes`` configuration file setting or ``config.include('pyramid_crow')``
2. Include a DSN in your config file as ``raven.dsn``

No special handling or explicit invocation is required, even if using an exception view.
``pyramid_crow`` automatically employs ``raven``'s password sanitization to strip sensitive values from submitted data.
The ``raven`` client is accessible as ``request.raven``.
Any configuration file values starting with ``raven.`` will be provided as keyword arguments when creating the client.
No automatic type conversion is performed; if any of the values you want to provide should be anything other than a string, you should convert them appropriately.

Ignoring Exceptions
-------------------

Not every exception needs to be captured by ``raven``.
Some – like ``pyramid.httpexceptions`` – indicate exceptional but expected conditions.
``pyramid_crow`` always ignores ``pyramid.httpexceptions``.
You can ignore other exceptions as well by providing a list of importable dotted names as ``pyramid_crow.ignore`` in your configuration.

For example::

  pyramid_crow.ignore =
    yourpackage.YourException
    yourpackage.YourOtherException
