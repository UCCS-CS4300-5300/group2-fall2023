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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Home import views as home_views

urlpatterns = [
    path("", home_views.Home.as_view(), name="index"),
    path("about-us/", home_views.About.as_view(), name="about"),
    path("profile/", home_views.Profile.as_view(), name="profile"),
    path("cart/", home_views.Cart.as_view(), name="cart"),

    path("markets/", include("Events.urls")),
    path("products/", include("Products.urls")),
    path("reservations/", include("Reservations.urls")),

    path("admin/", admin.site.urls),
    path("signup/", home_views.SignUp.as_view(), name="signup"),
    path("accounts/profile/", home_views.login_redirect),
    path("accounts/logout/", home_views.logout_request, name="logout"),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
