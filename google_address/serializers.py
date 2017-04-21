from google_address import models
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Address
    fields = ['raw', 'raw2', 'address_line', 'city_state']
    read_only_fields = ['address_line', 'city_state']


class AddressLatLngSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Address
    fields = ['raw', 'raw2', 'address_line', 'city_state', 'lat', 'lng']
    read_only_fields = ['address_line', 'city_state']


class AddressCityStateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Address
    fields = ['city_state']


