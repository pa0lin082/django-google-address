Settings
===============

All settings must be put inside a dictionary named GOOGLE_ADDRESS in your settings.py

API_KEY
~~~~~~~~~~~~~~~~

This is the Google Maps API key acquired through Google console.

Default: `None`

API_LANGUAGE
~~~~~~~~~~~~~~~~

The language which addresses will be requested in.

Default: `en_US`

ASYNC_CALLS
~~~~~~~~~~~~~~~~

When saving an `Address` object, a request will be made to Google Maps API to fetch address information. When set to `True`, this will make the requests asynchronous so you can return a response to the user without waiting for an API response.

Default: `False`

Example configuration
~~~~~~~~~~~~~~~~~~~~~
::

    GOOGLE_ADDRESS = {
      'API_KEY': 'BIzaSyFCcHqskKlpsUJ5jdQGVzdP-7uNu9O4g8w',
      'API_LANGUAGE': 'en_US'
    }
