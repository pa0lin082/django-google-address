from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp_core.models import Cause

class CauseInline(admin.TabularInline):
  model = Cause


class CauseAdmin(admin.ModelAdmin):
	fields = ['id', 'name']

	list_display = ['id', 'name']

	list_filter = []

	list_editable = ['name']

	search_fields = ['id', 'name']

	readonly_fields = ['id']

	raw_id_fields = []


admin.site.register(Cause, CauseAdmin)


