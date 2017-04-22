Getting Started
===============

The module is easy to use and you can get started with django-google-address in just a few minutes.

Installing
---------------

1. Install the module like any other python module::

    pip install django-google-address

2. Add it to `INSTALLED_APPS` on `settings.py`::

    INSTALLED_APPS = [
      ...,
      'google_address'
    ]
    
3. Migrate::
  
    ./manage.py migrate

Configuring
----------------

There are two settings you can and should use to make the module work correctly.
Here is an example of such configuration::

    GOOGLE_ADDRESS = {
      'API_KEY': 'BIzaSyFCcHqskKlpsUJ5jdQGVzdP-7uNu9O4g8w'
      'API_LANGUAGE': 'en_US'
    }

You can read more about configuring at :doc:`Settings <settings>` section.

Using
----------------

Create an Address object with the raw address. Requests will be made to the Google API when saving the address::

    >>> from google_address.models import Address
    >>> a = Address(raw="Av. Paulista, 1000")
    >>> a.save()
    >>> a.address_line
    'Avenida Paulista, 1000, Bela Vista, São Paulo, SP, Brazil'

You can easily use foreign keys to the model::
    
    class Building(models.Model):
      address = models.ForeignKey('google_address.Address')
