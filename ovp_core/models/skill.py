import vinaigrette
from django.db import models

from django.utils.translation import ugettext_lazy as _

class Skill(models.Model):
  name = models.CharField(_('name'), max_length=100)

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'ovp_core'
    verbose_name = _('skill')

vinaigrette.register(Skill, ['name'])
