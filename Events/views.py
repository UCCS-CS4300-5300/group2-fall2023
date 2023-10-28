### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.views import View
from django.shortcuts import render
from .models import Event

class EventsList(View):
    """ Get a list of Harvestly events. URL `/get-events-list/` """
    
    def get(self, request):
        """ Query all events, render in events list template. """

        # TODO
        # Query events
        events = Event.objects.all()
        # Pass events to events_list.html
        return render(request, "events_list.html", {'events': events})