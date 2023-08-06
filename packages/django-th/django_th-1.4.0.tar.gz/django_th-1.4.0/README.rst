.. image:: https://travis-ci.org/foxmask/django-th.svg?branch=master
    :target: https://travis-ci.org/foxmask/django-th
    :alt: Travis Status


.. image:: http://img.shields.io/pypi/v/django-th.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Latest version


.. image:: https://codeclimate.com/github/foxmask/django-th/badges/gpa.svg
    :target: https://codeclimate.com/github/foxmask/django-th
    :alt: Code Climate


.. image:: https://codeclimate.com/github/foxmask/django-th/badges/coverage.svg
   :target: https://codeclimate.com/github/foxmask/django-th/coverage
   :alt: Test Coverage


.. image:: https://scrutinizer-ci.com/g/foxmask/django-th/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/foxmask/django-th/?branch=master
   :alt: Scrutinizer Code Quality


.. image:: https://readthedocs.org/projects/trigger-happy/badge/?version=latest
    :target: https://readthedocs.org/projects/trigger-happy/?badge=latest
    :alt: Documentation status


.. image:: http://img.shields.io/badge/python-3.6-orange.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Python version supported


.. image:: http://img.shields.io/badge/license-BSD-blue.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: License


=============
Trigger Happy
=============

Automatically share data between popular services you use on the web.
And instead of giving your credentials to them, become the owner of yours !

For example a new RSS item is published, "Trigger Happy" will be able to
automatically create a note on your Evernote account or create a bookmark to
your own Wallabag or Pocket account and so on.


.. image:: https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg
    :target: https://saythanks.io/to/foxmask
    :alt: Say thanks to foxmask


Description
===========

The goal of this project is to be independent from any other solution like
IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without
depending on any non-free solution.

With this project you can host triggers for you.

All you need is to have a hosting provider (or simply your own server ;) )
who permits to use a manager of tasks like "cron" and, of course Python.


.. image:: https://trigger-happy.eu/static/th_esb.png
   :alt: Trigger Happy Architecture


Requirements
============

The minimum are the following :

* Python 3.6.x
* `DjangoRestFramework <http://www.django-rest-framework.org/>`_ == 3.6.2
* `Django <https://www.djangoproject.com/>`_ == 1.11
* `Arrow <https://pypi.python.org/pypi/arrow>`_ == 0.10.0
* `Django-formtools <https://pypi.python.org/pypi/django-formtools>`_ == 2.0
* `Django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.7.3
* `Django-Redis <https://pypi.python.org/pypi/django-redis/>`_ == 4.7.0
* `Pypandoc <https://pypi.python.org/pypi/pypandoc/>`_ == 1.3.3
* `Requests-oAuthlib <https://pypi.python.org/pypi/requests-oauthlib/>`_ == 0.8.0


Installation
============

.. code-block:: bash

    pip install django-th[all]


or to make your own "recipe" :


.. code-block:: bash

    pip install django-th[min]  # will just install RSS and Wallabag
    pip install django-th[rss,wallabag]
    pip install django-th[rss,wallabag,twitter,github]
    pip install django-th[all]



Documentation
=============

For installation and settings, see http://trigger-happy.readthedocs.org/


