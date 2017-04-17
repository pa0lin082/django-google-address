from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp_core.models import GoogleAddress


class GoogleAddressAdmin(admin.ModelAdmin):
  fields = [
    'id', 'typed_address', 'typed_address2'
  ]

  list_display = [
    'id', 'typed_address', 'typed_address2'
  ]

  list_filter = []

  list_editable = []

  search_fields = ['typed_address', 'typed_address2', 'address_line']

  readonly_fields = [
    'id'
  ]

  raw_id_fields = []


admin.site.register(GoogleAddress, GoogleAddressAdmin)


