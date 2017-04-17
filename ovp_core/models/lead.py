from django.db import models
from django.utils.translation import ugettext_lazy as _

class Lead(models.Model):
  name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
  email = models.CharField(_('Email'), max_length=100)
  phone = models.CharField(_('Phone'), max_length=30, null=True, blank=True)
  country = models.CharField(_('Country'), max_length=2, null=True, blank=True)

  class Meta:
    app_label = 'ovp_core'
    verbose_name = _('Lead')
    verbose_name_plural = _('Leads')
