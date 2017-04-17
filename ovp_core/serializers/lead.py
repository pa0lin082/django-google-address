from ovp_core import models
from rest_framework import serializers


class LeadSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ['name', 'email', 'phone', 'country']
    model = models.Lead
