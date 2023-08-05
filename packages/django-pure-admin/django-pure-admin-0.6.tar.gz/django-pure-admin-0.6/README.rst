==========
Django PURE ADMIN
==========
Step by step i will change admin template of Django. Some UI i will take from here: https://gurayyarar.github.io/AdminBSBMaterialDesign/

.. image:: http://res.cloudinary.com/responsivebreakpoints/image/upload/c_scale,w_555/v1505836384/Screen_Shot_2017-09-19_at_8.48.19_PM_kzwtuu.png
    :width: 500px
    :height: 500px
    :scale: 50%
    :alt: Login admin
    :align: center

.. image:: http://res.cloudinary.com/responsivebreakpoints/image/upload/c_scale,w_952/v1505836583/Screen_Shot_2017-09-19_at_8.48.03_PM_ktd6iz.png
    :width: 800px
    :height: 800px
    :scale: 50%
    :alt: App list
    :align: center

.. image:: http://res.cloudinary.com/responsivebreakpoints/image/upload/c_scale,w_849/v1505836653/Screen_Shot_2017-09-19_at_8.49.26_PM_qrkxbs.png
    :width: 800px
    :height: 800px
    :scale: 50%
    :alt: Change list
    :align: center

.. image:: http://res.cloudinary.com/responsivebreakpoints/image/upload/c_scale,w_1138/v1505836693/Screen_Shot_2017-09-19_at_8.50.31_PM_n31pq1.png
    :width: 800px
    :height: 800px
    :scale: 50%
    :alt: Change form
    :align: center

Installation
============
* Download and install latest version of Django Pure Admin:
.. code:: python

    pip install django-pure-admin

* Add 'pure_admin' application to the INSTALLED_APPS setting of your Django project settings.py file (note it should be before 'django.contrib.admin')::

    INSTALLED_APPS = [
        ...
        'pure_admin',
        'django.contrib.admin',
    ]


