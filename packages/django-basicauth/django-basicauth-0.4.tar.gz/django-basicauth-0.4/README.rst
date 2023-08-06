================
django-basicauth
================

Basic auth utilities for Django.

Requires
========

Tested under...

* Python

  * 2.7
  * 3.6

* Django

  * 1.8
  * 1.10
  * 1.11

Installation
============

::

    pip install django-basicauth


Usage
=====

.. code-block:: python

    from basicauth.decorators import basic_auth_required

    @basic_auth_required
    def myview(request):
        ...

or by a middleware.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'basicauth.middleware.BasicAuthMiddleware',
        ...
    )

Settings
========

* ``BASICAUTH_USERS`` (required): Dictionary including keys as username and values as passwords.
* ``BASICAUTH_REALM``: realm string, default is "Secure resource".
* ``BASICAUTH_DISABLE``: Disable all of barriers by this library.
