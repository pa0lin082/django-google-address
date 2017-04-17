from django.conf import settings
from django.utils.translation import ugettext as _


def get_settings(string="OVP_CORE"):
  return getattr(settings, string, {})
