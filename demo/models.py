from django.db import models
from google_address.fields import AddressField


class DemoObj(models.Model):

    address = AddressField()

