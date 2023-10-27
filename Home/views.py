### CS 4300 Fall 2023 Group 2
### Harvestly
### Home Views

from django.views import View
from django.shortcuts import render

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