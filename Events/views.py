### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Event

class EventsList(ListView):
    """ Get a list of Harvestly events. URL `/get-events-list/` """
    
    def get(self, request):
        """ Query all events, render in events list template. """

        # Query events
        model = Event.objects.all()
        template_name = "events_list.html"

        # Pass events to events_list.html
        return render(request, template_name, {'eventlist': model})