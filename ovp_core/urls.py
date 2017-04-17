from django.conf.urls import url, include

from ovp_core import views

urlpatterns = [
  url("^startup/$", views.startup, name="startup"),
  url("^contact/$", views.contact, name="contact"),
  url("^lead/$", views.record_lead, name="lead"),
]
