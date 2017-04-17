from rest_framework import response
from rest_framework import decorators
from rest_framework import status

from ovp_core import models
from ovp_core import serializers
from ovp_core import helpers
from ovp_core import emails
from django.utils import translation

@decorators.api_view(["GET"])
def startup(request):
  """ This view provides initial data to the client, such as available skills and causes """
  with translation.override(translation.get_language_from_request(request)):
    skills = serializers.SkillSerializer(models.Skill.objects.all(), many=True)
    causes = serializers.CauseSerializer(models.Cause.objects.all(), many=True)

    return response.Response({
      "skills": skills.data,
      "causes": causes.data
    })


@decorators.api_view(["POST"])
def contact(request):
  settings = helpers.get_settings()
  valid_emails = settings.get("VALID_CONTACT_RECIPIENTS", [])


  name = request.data.get("name", "")
  message = request.data.get("message", "")
  email = request.data.get("email", "")
  phone = request.data.get("phone", "")
  recipients = request.data.get("recipients", request.data.get("recipients[]", []))
  context = {"name": name, "message": message, "email": email, "phone": phone}

  if not type(recipients) is list:
    recipients = [recipients]

  # Check if all recipients are valid
  for recipient in recipients:
    if recipient not in valid_emails:
      return response.Response({"detail": "Invalid recipients."}, status.HTTP_400_BAD_REQUEST)


  contact = emails.ContactFormMail(recipients)
  contact.sendContact(context=context)

  return response.Response({"success": True})



from .models import Lead

@decorators.api_view(["POST"])
def record_lead(request):
  Lead.objects.create(
    name=request.data.get('name', None),
    email=request.data.get('email', None),
    phone=request.data.get('phone', None),
    country=request.data.get('country', None)
  )
  return response.Response({"success": True})
