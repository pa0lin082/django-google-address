from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
  class Meta:
    fields = []
