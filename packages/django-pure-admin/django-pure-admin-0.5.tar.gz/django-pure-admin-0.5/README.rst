==========
Django PURE ADMIN
==========
Step by step i will change admin template of Django. Some UI i will take from here: https://gurayyarar.github.io/AdminBSBMaterialDesign/

Installation
============
* Download and install latest version of Django Pure Admin:
.. code:: python
    pip install django-jet

* Add 'pure_admin' application to the INSTALLED_APPS setting of your Django project settings.py file (note it should be before 'django.contrib.admin')::

    INSTALLED_APPS = [
        ...
        'pure_admin',
        'django.contrib.admin',
    ]


