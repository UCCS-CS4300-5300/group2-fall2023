### CS 4300 Fall 2023 Group 2
### Harvestly
### Home Views

from django.views import View
from django.shortcuts import render, redirect
from harvestly.forms import CustomSignUpForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def logout_request(request):
    logout(request)
    return redirect("index")

def login_redirect(request):
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


