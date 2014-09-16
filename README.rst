django-fairepart
================

.. image:: https://secure.travis-ci.org/thoas/django-fairepart.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-fairepart

A generic application to import your contact from facebook, google, etc.

Compatibility
-------------

This library is compatible with:

- python2.6, django1.5
- python2.6, django1.6
- python2.7, django1.5
- python2.7, django1.6
- python2.7, django1.7

Installation
------------

1. Download the package on GitHub_ or simply install it via PyPi
2. Add ``fairepart`` to your ``INSTALLED_APPS`` ::

    INSTALLED_APPS = (
        'fairepart',
    )

3. Sync your database using ``syncdb`` command from django command line
4. Include ``fairepart`` in your ``urls.py`` ::

    from django.conf.urls import patterns, url, include

    urlpatterns = patterns(
        '',
        (r'^',
        include('fairepart.urls')),
    )

5. Configure settings

.. _GitHub: https://github.com/thoas/django-fairepart
