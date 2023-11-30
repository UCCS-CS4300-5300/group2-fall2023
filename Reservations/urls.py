### CS 4300 Fall 2023 Group 2
### Harvestly
### Reservation app routing

""" URL Configuration for Reservation App """

from django.urls import path
from . import views

urlpatterns = [
    path("new/<int:product_id>", views.ReservationCreate.as_view(), name="reservation-create"),
    path("edit/<int:pk>", views.ReservationUpdate.as_view(), name="reservation-update"),
    path("delete/<int:pk>", views.ReservationDelete.as_view(), name="reservation-delete"),
]
