'''This module contains the views for the Home app.'''
### CS 4300 Fall 2023 Group 2
### Harvestly
### Home Views

from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from Events.models import Event
from Products.models import Product
from Reservations.models import Reservation


@login_required
def logout_request(request):
    '''Handles logout functionality'''
    logout(request)
    return redirect("index")


def login_redirect(request):
    '''Basic redirect for login to redirect to the home page'''
    return redirect("index")


class Home(View):
    """ Harvestly home page. URL `/` """

    def get(self, request):
        """ Render home page. """

        return render(request, "home.html", )


class About(View):
    """ Harvestly home page. URL `/about-us` """

    def get(self, request):
        """ Render about page. """

        return render(request, "about.html", )


class SignUp(CreateView):
    """ Sign-up page. URL `/signup` """

    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class Profile(LoginRequiredMixin, View):
    """ User profile page for seeing events and products """

    def get(self, request):
        """ Handle get requests for profile """

        event_list = Event.objects.filter(organizer=request.user)
        product_list = Product.objects.filter(owner=request.user)

        return render(request, "profile.html", {
            "event_list": event_list,
            "product_list": product_list,
        })


class Cart(LoginRequiredMixin, View):
    """ User's cart of reserved prdocuts """

    def get(self, request):
        """ Handle get requests for user's cart """

        reservation_list = Reservation.objects.filter(customer=request.user)

        return render(request, "cart.html", {
            "reservation_list": reservation_list,
        })
