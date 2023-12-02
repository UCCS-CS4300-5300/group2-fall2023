# CS 4300 Fall 2023 Group 2
# Harvestly
# Test Events Models

""" URLs for Events application """

from django.urls import path
from . import views

urlpatterns = [
  path("", views.EventList.as_view(), name="events"),
  path("new", views.EventCreate.as_view(), name="event-create"),
  path("details/<int:pk>", views.EventDetail.as_view(), name="event-detail"),
  path("edit/<int:pk>", views.EventUpdate.as_view(), name="event-update"),
  path("delete/<int:pk>", views.EventDelete.as_view(), name="event-delete"),
]
