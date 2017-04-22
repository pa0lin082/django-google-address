Filtering
=========

Due to addresses structure in the database, you can easily filter them by any address component type. We recommend you get familiarized with the :doc:`model structure <models>` and Google Maps API `address components <https://developers.google.com/maps/documentation/geocoding/intro#Types>`_.

Examples
~~~~~~~~

Filtering by country
--------------------
::

    >> Address.objects.filter(address_components__long_name="Brazil", address_components__types__name="country")

Filtering by state
------------------
::

    >> Address.objects.filter(address_components__long_name="São Paulo", address_components__types__name="administrative_area_level_1")

Filtering by city
-----------------
::

    >> Address.objects.filter(address_components__long_name="São Paulo", address_components__types__name="locality")

Filtering by neighborhood
-------------------------
::

    >> Address.objects.filter(address_components__long_name="Bela Vista", address_components__types__name__in=["neighborhood", "sublocality_level_1"])
