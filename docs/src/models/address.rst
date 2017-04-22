Address
===============

The Address model is the reason for this module to exist.

Creating objects
~~~~~~~~~~~~~~~~

While creating Address objects, you can set raw and raw2 fields.

`raw` field is the address that may include street name, number, neighborhood, city, state and country. `raw2` is any extra data you might want to include with the address, such as an apartment number.

When the object `save` method is called, a request is made to Google Maps API to fetch information about the address.

Existing objects
~~~~~~~~~~~~~~~~

After an addres is saved, you can access a few extra fields such as `address_line`, `city_state`, `lat` and `lng`

Example
~~~~~~~~~~~~~~~~
::

    >>> from google_address.models import Address
    >>> a = Address(raw="Av. Paulista, 1000", raw2="Room number 101")
    >>> a.save()
    >>> a.address_line
    'Avenida Paulista, 1000, Bela Vista, São Paulo, SP, Brazil'
    >>> a.city_state
    'São Paulo, SP'
    >>> (a.lat, a.lng)
    (-23.5647577, -46.6518495)


Fields
~~~~~~
::

    class Address(models.Model):
      raw = models.CharField(max_length=400, blank=True, null=True)
      raw2 = models.CharField(max_length=400, blank=True, null=True)
      address_line = models.CharField(max_length=400, blank=True, null=True)
      city_state = models.CharField(max_length=400, blank=True, null=True)
      lat = models.FloatField('lat', blank=True, null=True)
      lng = models.FloatField('lng', blank=True, null=True)
      address_components = models.ManyToManyField(AddressComponent)
