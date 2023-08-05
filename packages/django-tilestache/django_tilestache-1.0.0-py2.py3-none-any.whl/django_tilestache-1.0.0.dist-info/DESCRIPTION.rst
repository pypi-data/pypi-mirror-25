=============================
Django TileStache
=============================

.. image:: https://badge.fury.io/py/django-tilestache.svg
    :target: https://badge.fury.io/py/django-tilestache

.. image:: https://travis-ci.org/george-silva/django-tilestache.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-tilestache

.. image:: https://codecov.io/gh/george-silva/django-tilestache/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-tilestache

Command and Control Center for Tilestache, inside a django app.

TileStache is a marvelous piece of software that can serve all kinds
of map tiles.

Our difficulty is that we needed a dynamic configuration for it, so we
created something integrated with Django, to act as command and control
center for it.

Basically the goal of this project is to have a Django app that can
configure TileStache. After that, we can serve some tiles from Django,
using the same configuration or use an array of TileStache servers to
it for us.

There are two main parts here:

* The configuration edition/storage/serialization;
* The command and control center;

Documentation
-------------

TODO

Quickstart
----------

Install Django TileStache::

    pip install django-tilestache

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_tilestache.apps.DjangoTilestacheConfig',
        ...
    )

Add Django TileStache's URL patterns:

.. code-block:: python

    from django_tilestache import urls as django_tilestache_urls


    urlpatterns = [
        ...
        url(r'^', include(django_tilestache_urls)),
        ...
    ]

This is optional. We have a few views that you can configure yourself. You don't need to follow our URL scheme.

Usage
-----

Layers
======

It's simple:

.. code-block:: python

    from django_tilestache.models import Layer

    layer = Layer.objects.create(
        **{
            'name': 'foolayer'  # this is the tilestache layer name
            'provider': {

            },  # tilestache provider options
            '...' : 'foo' # all other options
        }
    )

Caches
======

TODO

Views
=====

There are two main views for django-tilestache. One is for serving the configuration and the other is for
serving tiles.

These views are not secured. It's your responsibility to configure these DRF APIViews with the
authentication and authorizations.

The configuration view will output a valid Tilestache JSON configuration.

The tile view will output a tile, depending on the registered configuration (caches and layers).

Cache management
================

You can use the CacheManager object to manage the cache
for your tilestache.

All you need to do is pass along the correct configuration
for it and use the methods, passing along geometries.

The CacheManager will take care of it. As long as your conf
is correct, it should do the correct thing.

How to run a tilestache server with the custom config?
======================================================

You can only use WSGI for now to do it.

Using gunicorn, here is a simple example:

.. code-block:: bash

    gunicorn "django_tilestache:RemoteTileStache('http://localhost:8000/api/tilestache/')" -b localhost:8080 --log-level=DEBUG

You can pass along other options as well, such as authentication
information. **Dont forget to secure your configuration view!**

Features
--------

* Cache management (seed and purge)
* Store tilestache layers in django models
* Custom tilestache server that looksup for configuration in a remote server
* Endpoint for serving the tilestache configuration
* Endpoint for serving the tilestache tiles, from Django

Roadmap
-------

* Management commands (generate conf, purge/seed cache, etc);
* Allow to use the Django cache settings instead of defining your own again
* Allow simple definition of layers using a Django style declarative configuration, like so:

.. code-block:: python

    class FooModel(models.Model):
        name = models.CharField(max_length=128)
        geom = models.PointField()
        class Meta:
            tilestache = (
                {'name': 'foo-layer-a', 'provider': 'foo'},
                {'name': 'foo-layer-b', 'provider': 'bar'}
            )


Uploading new distros
---------------------

.. code-block:: bash

    bumpversion --current-version x.x.x minor
    make release
    git push origin master --tags


Running Tests
-------------

Does the code actually work?

.. code-block:: python

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

WARNING: not fully tested with tox YET.

It's tested and working for Django 1.11 and Python 2.7.

Credits
-------

Tools used in rendering this package:

* `SIGMA Geosistemas`_
* TileStache_
*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _SIGMA Geosistemas: https://sigmageosistemas.com.br
.. _TileStache: http://tilestache.org
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.6.0 (2017-05-30)

* First **actual release** on PyPI.
* New TileStache server that can ping a configuration URL and
self configure.
* Layer model and all the serializers needed to make this work
using Django REST Framework
* REST View to handle fecthing the configuration from the database
* REST View to serve tiles from Django

0.1.0 (2017-04-24)
++++++++++++++++++

* First release on PyPI.


