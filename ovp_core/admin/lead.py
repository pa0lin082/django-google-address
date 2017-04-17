from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

import csv
from django.http import HttpResponse

from ovp_core.models import Lead


def export_all_as_csv(model_admin, request, queryset):
	if not request.user.is_staff:
		raise PermissionDenied

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="leads.csv"'

	csv_writer = csv.writer(response)
	for lead in queryset.all():
		csv_writer.writerow([lead.email, lead.name or '', lead.phone or '', lead.country or ''])

	return response


class LeadAdmin(admin.ModelAdmin):
	fields = ['id', 'name', 'email', 'phone']
	list_display = ['id', 'name', 'email', 'phone']
	list_filter = []
	list_editable = ['name']
	search_fields = ['id', 'name', 'email', 'phone']
	readonly_fields = ['id']
	raw_id_fields = []

	actions = [export_all_as_csv]

	def changelist_view(self, request, extra_context=None):
		if 'action' in request.POST and request.POST['action'] == 'export_all_as_csv':
			if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
				post = request.POST.copy()
				for u in Lead.objects.all():
					post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
				request._set_post(post)
		return super(LeadAdmin, self).changelist_view(request, extra_context)

admin.site.register(Lead, LeadAdmin)


