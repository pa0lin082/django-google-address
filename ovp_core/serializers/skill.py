from ovp_core import models
from ovp_core import validators
from rest_framework import serializers


class SkillSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ['id', 'name']
    model = models.Skill

class SkillAssociationSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField()
  name = serializers.CharField(read_only=True)

  class Meta:
    fields = ['id', 'name']
    model = models.Skill
    validators = [validators.skill_exist]
