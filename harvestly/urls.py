### CS 4300 Fall 2023 Group 2
### Harvestly

"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from Home import views as home_views
from Events import views as events_views

urlpatterns = [
    # TODO - Not sure how this needs to be updated for login
    path("", home_views.Home.as_view(), name="index"),
    path("events-list/", events_views.EventsList.as_view(), name="events-list"),
]
