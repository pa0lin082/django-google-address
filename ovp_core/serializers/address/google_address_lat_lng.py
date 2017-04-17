from ovp_core import models
from rest_framework import serializers


class GoogleAddressLatLngSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.GoogleAddress
    fields = ['typed_address', 'typed_address2', 'address_line', 'city_state', 'lat', 'lng']
    read_only_fields = ['address_line', 'city_state']
