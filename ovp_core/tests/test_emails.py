from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail

import ovp_core.emails

class TestBaseMail(TestCase):
  def test_email_trigger(self):
    """Assert that email is sent to outbox"""
    bm = ovp_core.emails.BaseMail('a@b.c')
    bm.sendEmail('base', '', {})
    self.assertTrue(len(mail.outbox) > 0)

  def test_async_email_trigger(self):
    """Assert that async emails are sent to outbox"""
    bm = ovp_core.emails.BaseMail('a@b.c', async_mail=True)
    bm.sendEmail('base', '', {}).join()
    self.assertTrue(len(mail.outbox) > 0)

  @override_settings(OVP_EMAILS={'base': {'disabled': True}})
  def test_email_can_be_disabled(self):
    """Assert that email can be disabled"""
    bm = ovp_core.emails.BaseMail('a@b.c')
    bm.sendEmail('base', '', {})
    self.assertTrue(len(mail.outbox) == 0)

  @override_settings(OVP_EMAILS={'base': {'subject': 'overriden'}})
  def test_email_subject_can_be_overridden(self):
    """Assert that email subject can be overridden"""
    bm = ovp_core.emails.BaseMail('a@b.c')
    bm.sendEmail('base', 'test', {})
    self.assertTrue(mail.outbox[0].subject == 'overriden')
