from django.apps import apps


from google_address.models import Address, AddressComponent

modeltranslation_installed = apps.is_installed("modeltranslation")

try:
    from modeltranslation.translator import register, TranslationOptions
except:
    raise Exception('translation.py is used by django-modeltranslation')


@register(AddressComponent)
class AddressComponentTranslationOptions(TranslationOptions):
    fields = ('long_name', 'short_name',)