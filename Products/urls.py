from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='products'),
#   path('new', views.EventCreate.as_view(), name='event-create'),
#   path('<int:pk>', views.EventDetail.as_view(), name='event-detail'),
#   path('<int:pk>/update', views.EventUpdate.as_view(), name='event-update'),
#   path('<int:pk>/delete', views.EventDelete.as_view(), name='event-delete'),
]