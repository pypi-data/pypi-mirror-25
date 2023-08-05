|Python| |Django| |License| |PyPI| |Build Status| |Coverage Status|

Django-Celery-GrowthMonitor
===========================

A Django helper to monitor jobs running Celery tasks

Features
--------

-  Utilities to track progress of Celery tasks via in-database jobs

Requirements
------------

-  Python >= 3.4
-  Django >= 1.8.18
-  Celery >= 4.0.2
-  ``django-echoices`` >=2.5.0
-  ``django-autoslug`` >=1.9.3

Installation
------------

Using PyPI
~~~~~~~~~~

1. Run ``pip install django-celery-growthmonitor``

Using the source code
~~~~~~~~~~~~~~~~~~~~~

1. Make sure ```pandoc`` <http://pandoc.org/index.html>`__ is installed
2. Run ``./pypi_packager.sh``
3. Run
   ``pip install dist/django_celery_growthmonitor-x.y.z-[...].wheel``,
   where ``x.y.z`` must be replaced by the actual version number and
   ``[...]`` depends on your packaging configuration

Usage
-----

TODO

.. |Python| image:: https://img.shields.io/badge/Python-3.4,3.5,3.6-blue.svg?style=flat-square
   :target: /
.. |Django| image:: https://img.shields.io/badge/Django-1.8,1.9,1.10,1.11-blue.svg?style=flat-square
   :target: /
.. |License| image:: https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square
   :target: /LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/django_celery_growthmonitor.svg?style=flat-square
   :target: https://pypi.org/project/django-celery-growthmonitor
.. |Build Status| image:: https://travis-ci.org/mbourqui/django-celery-growthmonitor.svg?branch=master
   :target: https://travis-ci.org/mbourqui/django-celery-growthmonitor
.. |Coverage Status| image:: https://coveralls.io/repos/github/mbourqui/django-celery-growthmonitor/badge.svg?branch=master
   :target: https://coveralls.io/github/mbourqui/django-celery-growthmonitor?branch=master


