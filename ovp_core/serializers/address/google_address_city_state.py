from ovp_core import models
from rest_framework import serializers


class GoogleAddressCityStateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.GoogleAddress
    fields = ['city_state']

