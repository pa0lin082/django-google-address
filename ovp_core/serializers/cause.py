from ovp_core import models
from ovp_core import validators
from rest_framework import serializers


class CauseSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ['id', 'name']
    model = models.Cause

class CauseAssociationSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField()
  name = serializers.CharField(read_only=True)

  class Meta:
    fields = ['id', 'name']
    model = models.Cause
    validators = [validators.cause_exist]
