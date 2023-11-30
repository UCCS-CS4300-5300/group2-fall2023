### CS 4300 Fall 2023 Group 2
### Harvestly
### Product app routing

""" URL Configuration for Products App """

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="products"),
    path("new", views.ProductCreate.as_view(), name="product-create"),
    path("new/<int:event_id>", views.ProductCreate.as_view(), name="product-create-with-event"),
    path("details/<int:pk>", views.ProductDetail.as_view(), name="product-details"),
    path("edit/<int:pk>", views.ProductUpdate.as_view(), name="product-update"),
    path("delete/<int:pk>", views.ProductDelete.as_view(), name="product-delete"),
]
