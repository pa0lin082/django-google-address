from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from google_address import helpers

import os
import requests

class AddressComponentType(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class AddressComponent(models.Model):
  long_name = models.CharField(max_length=400)
  short_name = models.CharField(max_length=400)
  types = models.ManyToManyField(AddressComponentType)

  def __str__(self):
    return self.long_name

class GoogleRegion(models.Model):
  region_name = models.CharField(max_length=400)
  filter_by = models.CharField(max_length=400)

class GoogleAddress(models.Model):
  raw = models.CharField(max_length=400, blank=True, null=True)
  raw2 = models.CharField(max_length=400, blank=True, null=True)
  address_line = models.CharField(max_length=400, blank=True, null=True)
  city_state = models.CharField(max_length=400, blank=True, null=True)
  lat = models.FloatField('lat', blank=True, null=True)
  lng = models.FloatField('lng', blank=True, null=True)
  address_components = models.ManyToManyField(AddressComponent)

  def get_city_state(self):
    state = self.address_components.filter(types__name='administrative_area_level_1')
    county = self.address_components.filter(types__name='administrative_area_level_2')
    locality = self.address_components.filter(types__name='locality')

    s = u""
    if locality.count():
      s += u"{}, ".format(locality[0].long_name)
    elif county.count():
      s += u"{}, ".format(county[0].long_name)

    if state.count():
      s += state[0].short_name

    return s

  def get_address(self):
    # Components types for address
    address = {'route': '', 'sublocality_level_1': '', 'administrative_area_level_2': '', 'administrative_area_level_1': '', 'country': '', 'street_number': ''}

    # Fill address dict
    for component in self.address_components.all():
      for component_type in component.types.all():
        if component_type.name in address:
          address[component_type.name] = {'short_name': component.short_name, 'long_name': component.long_name}

    # Build address string
    string_address = ''
    if 'route' in address and isinstance(address['route'], dict):
      string_address += '{}, '.format(address['route']['long_name'])
    if 'route' in address and isinstance(address['street_number'], dict):
      string_address += '{}, '.format(address['street_number']['long_name'])
    if 'sublocality_level_1' in address and isinstance(address['sublocality_level_1'], dict):
      string_address += '{}, '.format(address['sublocality_level_1']['long_name'])
    if 'administrative_area_level_2' in address and isinstance(address['administrative_area_level_2'], dict):
      string_address += '{}, '.format(address['administrative_area_level_2']['long_name'])
    if 'administrative_area_level_1' in address and isinstance(address['administrative_area_level_1'], dict):
      string_address += '{}, '.format(address['administrative_area_level_1']['short_name'])
    if 'country' in address and isinstance(address['country'], dict):
      string_address += '{}, '.format(address['country']['long_name'])

    string_address = string_address.strip().strip(',')

    return string_address

  def get_country_code(self):
    try:
      return self.address_components.filter(types__name='country').first().short_name.lower()
    except (AttributeError):
      return None

  def __str__(self):
    if self.address_line:
      return self.address_line
    return ""


@receiver(post_save, sender=GoogleAddress)
def update_address(sender, instance, **kwargs):
  if kwargs.get('raw', False): # pragma: no cover
    return None

  settings = helpers.get_settings()
  maps_language = settings.get('MAPS_API_LANGUAGE', 'en_US')

  addressline = instance.raw

  url = 'https://maps.googleapis.com/maps/api/geocode/json?language={}&address={}'.format(maps_language, addressline)

  key = os.environ.get('GOOGLE_MAPS_KEY', None)
  if key: #pragma: no cover
    url = '{}&key={}'.format(url, key)

  r = requests.get(url)
  data = r.json()

  # Iterate through address components
  instance.address_components.clear()
  if len(data['results']) > 0:
    for component in data['results'][0]['address_components']:
    # TODO: Do not work only with first result
      # Look for component with same name and type
      ac = AddressComponent.objects.annotate(count=Count('types')).filter(long_name=component['long_name'], short_name=component['short_name'])
      for component_type in component['types']:
        ac = ac.filter(types__name=component_type)
      ac = ac.filter(count=len(component['types']))

      if not ac.count():
      # Component not found, creating
        ac = AddressComponent(long_name=component['long_name'], short_name=component['short_name'])
        ac.save()
      else:
        ac = ac.first()
        ac.types.clear()
        ac.save()


      # Add types for component
      for ctype in component['types']:
        try:
          at = AddressComponentType.objects.get(name=ctype)
        except ObjectDoesNotExist:
          at = AddressComponentType(name=ctype)
          at.save()
        ac.types.add(at)

      instance.address_components.add(ac)

    try:
      if data['results'][0]['geometry']:
        GoogleAddress.objects.filter(pk=instance.pk).update(lat=data['results'][0]['geometry']['location']['lat'], lng=data['results'][0]['geometry']['location']['lng'])
    except: #pragma: no cover
      pass

    # Using update to avoid post_save signal
    GoogleAddress.objects.filter(pk=instance.pk).update(address_line=instance.get_address(), city_state=instance.get_city_state())
    #update_searchindex(instance)
