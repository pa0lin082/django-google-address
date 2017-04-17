from django.test import TestCase

# Just import to test execution
from ovp_core import validators

class TestAddressValidator(TestCase):
  def test_validation_functionn(self):
    """Assert that address_validate doesn't raise exception on valid address"""
    validators.address_validate({'typed_address': 'R. Abc'})
