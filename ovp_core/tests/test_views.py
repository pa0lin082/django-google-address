from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail
from django.utils import translation

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_core import models
from ovp_core import serializers

class TestStartupView(TestCase):
  def setUp(self):
    self.skills_data = serializers.SkillSerializer(models.Skill.objects.all(), many=True).data
    self.causes_data = serializers.CauseSerializer(models.Cause.objects.all(), many=True).data

  def test_returns_startup_data(self):
    """ Test startup route returns skills and causes """
    client = APIClient()
    response = client.get(reverse("startup"), format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["skills"] == self.skills_data)
    self.assertTrue(response.data["causes"] == self.causes_data)

  def test_returns_localized_startup_data(self):
    """ Test startup route returns skills and causes """
    client = APIClient(HTTP_ACCEPT_LANGUAGE="pt-br")
    response = client.get(reverse("startup"), format="json")

    with translation.override('pt-br'):
      skills_data = serializers.SkillSerializer(models.Skill.objects.all(), many=True).data
      causes_data = serializers.CauseSerializer(models.Cause.objects.all(), many=True).data
      self.assertTrue(response.status_code == 200)
      self.assertTrue(response.data["skills"] == skills_data)
      self.assertTrue(response.data["causes"] == causes_data)


class TestContactFormView(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.basis_data = {"name": "my-name", "message": "my message", "email": "reply_to@asddsa.com", "phone": "+5511912345678"}

  @override_settings(OVP_CORE={"VALID_CONTACT_RECIPIENTS": []})
  def test_cant_send_invalid_recipient(self):
    """ Test sending contact form to invalid recipient does not work """
    data = self.basis_data

    data["recipients"] = ["invalid@recipient.com"]
    response = self.client.post(reverse("contact"), data=data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["detail"] == "Invalid recipients.")
    self.assertTrue(len(mail.outbox) == 0)

    data["recipients"] = ["testemail@1.com", "invalid@recipient.com"]
    response = self.client.post(reverse("contact"), data=data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["detail"] == "Invalid recipients.")
    self.assertTrue(len(mail.outbox) == 0)

  @override_settings(OVP_CORE={"VALID_CONTACT_RECIPIENTS": ["testemail@1.com"]})
  def test_can_send_valid_recipient(self):
    """ Test sending contact form to valid recipient does work """
    data = self.basis_data
    data["recipients"] = ["testemail@1.com"]

    response = self.client.post(reverse("contact"), data=data, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(len(mail.outbox) == 1)
    self.assertTrue(data["name"] in mail.outbox[0].body)
    self.assertTrue(data["message"] in mail.outbox[0].body)
    self.assertTrue(data["email"] in mail.outbox[0].body)
    self.assertTrue(data["phone"] in mail.outbox[0].body)

  @override_settings(OVP_CORE={"VALID_CONTACT_RECIPIENTS": ["testemail@1.com", "testemail@2.com"]})
  def test_can_send_multiple_valid_recipients(self):
    """ Test sending contact form to multiple valid recipient does work """
    data = self.basis_data
    data["recipients"] = ["testemail@1.com", "testemail@2.com"]

    response = self.client.post(reverse("contact"), data=data, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(len(mail.outbox) == 2)
