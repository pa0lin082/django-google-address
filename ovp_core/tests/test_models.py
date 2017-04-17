from django.test import TestCase
from django.test.utils import override_settings

from ovp_core.models import GoogleAddress
from ovp_core.models import AddressComponent
from ovp_core.models import AddressComponentType
from ovp_core.models import Skill
from ovp_core.models import Cause

def remove_component(address, types):
  for component in address.address_components.all():
    for type in component.types.all():
      if type.name in types:
        component.delete()

  return address


class GoogleAddressModelTestCase(TestCase):
  @override_settings(OVP_CORE={'MAPS_API_LANGUAGE': 'en_US'})
  def test_api_call(self):
    """Assert GoogleAddress calls google API and get address"""
    a = GoogleAddress(typed_address="Rua Teçaindá, 81, SP", typed_address2="Casa")
    a.save()

    a = GoogleAddress.objects.get(pk=a.pk)
    self.assertTrue(a.typed_address == "Rua Teçaindá, 81, SP")
    self.assertTrue(a.typed_address2 == "Casa")
    self.assertTrue(a.address_line == "Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil")
    self.assertTrue(a.__str__() == "Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil")
    self.assertTrue(a.lat)
    self.assertTrue(a.lng)

    a.typed_address="Rua Capote Valente, 701, SP"
    a.save()
    a = GoogleAddress.objects.get(pk=a.pk)
    self.assertTrue(a.typed_address == "Rua Capote Valente, 701, SP")
    self.assertTrue(a.typed_address2 == "Casa")
    self.assertTrue(a.address_line == "Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil")
    self.assertTrue(a.__str__()  == "Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil")
    self.assertTrue(a.lat)
    self.assertTrue(a.lng)

    a.address_line=None
    self.assertTrue(a.__str__() == "")

  def test_locality(self):
    """Assert GoogleAddressModel.get_city_state preference order is locality, administrative_area_2"""
    a = GoogleAddress(typed_address="Chicago")
    a.save()
    self.assertTrue("Chicago" in a.get_city_state())

    a = remove_component(a, ['locality'])
    self.assertTrue("Cook" in a.get_city_state())


class AddressComponentTypeModelTestCase(TestCase):
  def test_str_call(self):
    """Assert AddressComponentType __str__ returns name"""
    a = AddressComponentType(name="xyz")
    a.save()

    self.assertTrue(a.__str__() == "xyz")

class AddressComponentModelTestCase(TestCase):
  def test_str_call(self):
    """Assert AddressComponent __str__ returns long name"""
    a = AddressComponent(short_name="short", long_name="long")
    a.save()

    self.assertTrue(a.__str__() == "long")

class SkillModelTestCase(TestCase):
  def test_name_max_length(self):
    """ Assert skill name can't be longer than 100 """
    n = "a" * 100
    s = Skill(name=n)
    s.full_clean()
    s.save()

    self.assertTrue(s.id > 0)

    n = ("a" * 101)
    s = Skill(name=n)

    with self.assertRaises(Exception) as context:
      s.full_clean()

    self.assertTrue('Ensure this value has at most 100 characters' in str(context.exception))


  def test_str_method_returns_name(self):
    """ Assert skill __str__ method returns name """
    n = "a" * 100
    s = Skill(name=n)
    s.save()

    self.assertTrue(s.__str__() == n)

class CauseModelTestCase(TestCase):
  def test_name_max_length(self):
    """ Assert cause name can't be longer than 100 """
    n = "a" * 100
    c = Cause(name=n)
    c.full_clean()
    c.save()

    self.assertTrue(c.id > 0)

    n = ("a" * 101)
    c = Cause(name=n)

    with self.assertRaises(Exception) as context:
      c.full_clean()

    self.assertTrue('Ensure this value has at most 100 characters' in str(context.exception))


  def test_str_method_returns_name(self):
    """ Assert cause __str__ method returns name """
    n = "a" * 100
    c = Cause(name=n)
    c.save()

    self.assertTrue(c.__str__() == n)
