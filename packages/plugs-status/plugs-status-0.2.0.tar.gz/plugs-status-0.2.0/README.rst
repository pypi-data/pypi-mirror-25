=============================
Plugs Status
=============================

.. image:: https://badge.fury.io/py/plugs-status.png
    :target: https://badge.fury.io/py/plugs-status

.. image:: https://travis-ci.org/ricardolobo/plugs-status.png?branch=master
    :target: https://travis-ci.org/ricardolobo/plugs-status

API Status endpoint

Documentation
-------------

The full documentation is at https://plugs-status.readthedocs.io.

Quickstart
----------

Install Plugs Status::

    pip install plugs-status

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_status.apps.PlugsStatusConfig',
        ...
    )

Add Plugs Status's URL patterns:

.. code-block:: python

    from plugs_status import urls as plugs_status_urls


    urlpatterns = [
        ...
        url(r'^', include(plugs_status_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
