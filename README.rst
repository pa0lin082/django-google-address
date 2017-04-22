======================
Django Google Address
======================

.. image:: https://img.shields.io/codeship/1e437ad0-05f2-0135-5add-32bab775782c/master.svg?style=flat-square
  :target: https://img.shields.io/codeship/1e437ad0-05f2-0135-5add-32bab775782c/master.svg?style=flat-square
.. image:: https://img.shields.io/codecov/c/github/leonardoarroyo/django-google-address.svg?style=flat-square
  :target: https://codecov.io/gh/leonardoarroyo/django-google-address
.. image:: https://readthedocs.org/projects/django-google-address/badge/?version=stable&style=flat-square
  :target: https://django-google-address.readthedocs.io/en/stable/
.. image:: https://img.shields.io/pypi/v/django-google-address.svg?style=flat-square
  :target: https://pypi.python.org/pypi/django-google-address/

Address model backed by Google Maps API for your project.

Getting Started
---------------
Installing
""""""""""""""
1. Install django-google-address::

    pip install django-google-address

2. Add it to `INSTALLED_APPS` on `settings.py`::

    INSTALLED_APPS = [
      ...,
      'google_address'
    ]

3. Migrate::
  
    ./manage.py migrate


Using
""""""""""""""

Create an Address object with the raw address. Requests will be made to the Google API when saving the address::

    >>> from google_address.models import Address
    >>> a = Address(raw="Av. Paulista, 1000")
    >>> a.save()
    >>> a.address_line
    'Avenida Paulista, 1000, Bela Vista, São Paulo, SP, Brazil'

Documentation
---------------

You can check the complete documentation `here <http://django-google-address.readthedocs.io/en/stable/>`_.

Testing
---------------
To test this module

::

  python google_address/tests/runtests.py

Versioning
---------------
We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/leonardoarroyo/django-google-address/tags>`_. 

License
---------------
This project is licensed under the MIT License. See the `LICENSE.md <https://github.com/leonardoarroyo/django-google-address/blob/master/LICENSE.md>`_ file for details.
