### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.views import View
from django.shortcuts import render

class EventsList(View):
    """ Get a list of Harvestly events. URL `/get-events-list/` or '/' """
    
    def get(self, request):
        """ Query all movies, format render in HTML. """

        # TODO
        # Query events
        # Pass events to events_list.html

        return render(request, "events_list.html", )