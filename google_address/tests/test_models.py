from django.test import TestCase
from django.test.utils import override_settings
from django.core.exceptions import ValidationError

from google_address.models import Address
from google_address.models import AddressComponent
from google_address.models import AddressComponentType
from google_address.fields import AddressField

from demo.models import DemoObj


def remove_component(address, types):
    for component in address.address_components.all():
        for type in component.types.all():
            if type.name in types:
                component.delete()

    return address


@override_settings(GOOGLE_ADDRESS={'API_LANGUAGE': 'en_US'})
class AddressModelTestCase(TestCase):
    def test_api_call(self):
        """Assert Address calls google API and get address"""
        a = Address(raw="Rua Teçaindá, 81, SP", raw2="Casa")
        a.save()

        a = Address.objects.get(pk=a.pk)
        self.assertTrue(a.raw == "Rua Teçaindá, 81, SP")
        self.assertTrue(a.raw2 == "Casa")
        self.assertTrue(a.address_line == "Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil")
        self.assertTrue(a.__str__() == "Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil")
        self.assertTrue(a.lat)
        self.assertTrue(a.lng)

    def test_api_call_2(self):
        a = Address(raw2="Casa")
        a.raw = "Rua Capote Valente, 701, SP"
        a.save()
        a = Address.objects.get(pk=a.pk)
        self.assertTrue(a.raw == "Rua Capote Valente, 701, SP")
        self.assertTrue(a.raw2 == "Casa")
        self.assertTrue(a.address_line == "Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil")
        self.assertTrue(a.__str__() == "Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil")
        self.assertTrue(a.lat)
        self.assertTrue(a.lng)

        a.address_line = None
        self.assertTrue(a.__str__() == "")

    def test_locality(self):
        """Assert AddressModel.get_city_state preference order is locality, administrative_area_2"""
        a = Address(raw="Chicago")
        a.save()
        self.assertTrue("Chicago" in a.get_city_state())

        a = remove_component(a, ['locality'])
        self.assertTrue("Cook" in a.get_city_state())

    def test_no_country(self):
        """Assert AddressModel.get_country_code returns None instead of rasing AttributeError if no country exists"""
        a = Address(raw="Chicago")
        a.save()

        AddressComponent.objects.all().delete()

        self.assertTrue(a.get_country_code() == None)

    def test_signal_returns_in_case_of_no_result(self):
        """Assert AddressModel.get_country_code returns None instead of rasing AttributeError if no country exists"""
        a = Address(raw="abcdefghijklmnopqrstuvwxyz")
        a.save()
        self.assertTrue(a.address_line == None)

    def test_region(self):
        a = Address(raw='Lombardia')
        a.save()
        print(a.__dict__)

    @override_settings(GOOGLE_ADDRESS={'API_LANGUAGE': 'it_IT'})
    def test_region_localized(self):
        a = Address(raw='Lombardia')
        a.save()
        print(a.__dict__)


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


class AddressFieldTestCase(TestCase):

    def test_address_field_constructor(self):
        field_instance = AddressField(null=True, blank=True)
        name, path, args, kwargs = field_instance.deconstruct()
        new_instance = AddressField(*args, **kwargs)

        self.assertEqual(field_instance.null, new_instance.null)

    def test_address_field_from_string(self):
        d = DemoObj()
        d.address = 'via villoresi 24'
        d.save()
        assert isinstance(d.address, Address)

    def test_address_field_from_pk(self):

        with self.assertRaises(ValidationError):
            d = DemoObj()
            d.address = 1
            d.save()

        a = Address(raw='Lombardia')
        a.save()

        d = DemoObj()
        d.address = a.pk
        d.save()
        assert isinstance(d.address, Address)
        assert d.address == a

        d = DemoObj.objects.last()
        assert isinstance(d.address, Address)
        assert d.address == a



