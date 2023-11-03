### CS 4300 Fall 2023 Group 2
### Harvestly
### Product app routing

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="products"),
    path("new", views.ProductCreate.as_view(), name="create-product"),
#   path('<int:pk>', views.EventDetail.as_view(), name='event-detail'),
#   path('<int:pk>/update', views.EventUpdate.as_view(), name='event-update'),
#   path('<int:pk>/delete', views.EventDelete.as_view(), name='event-delete'),
]