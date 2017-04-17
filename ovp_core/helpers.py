from django.conf import settings
from django.utils.translation import ugettext as _


def get_settings(string="OVP_CORE"):
  return getattr(settings, string, {})


def is_email_enabled(email):
  """ Emails are activated by default. Returns false
      if an email has been disabled in settings.py
  """
  s = get_settings(string="OVP_EMAILS")
  email_settings = s.get(email, {})

  enabled = True
  if email_settings.get("disabled", False):
    enabled = False

  return enabled


def get_email_subject(email, default):
  """ Allows for email subject overriding from settings.py  """
  s = get_settings(string="OVP_EMAILS")
  email_settings = s.get(email, {})

  title = email_settings.get("subject", default)

  return _(title)
