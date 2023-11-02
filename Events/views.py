### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.shortcuts import render
from .models import Event
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class EventsList(ListView):
    """ Get a list of Harvestly events. URL `/get-events-list/` """
    
    def get(self, request):
        """ Query all events, render in events list template. """

        # Query events
        model = Event.objects.all()
        template_name = "event_list.html"

        # Pass events to events_list.html
        return render(request, template_name, {'eventlist': model})
    
class EventDetail(DetailView):
    def create_event(self, request):
        model = self
        template_name = "event_create.html"

        # Pass event to events_create.html
        return render(request, template_name, {'event': model})
class EventCreate(CreateView):
    def update_event(self, request):
        model = self
        template_name = "event_update.html"

        # Pass event to events_update.html
        return render(request, template_name, {'event': model})
class EventUpdate(UpdateView):
    def get_event(self, request):
        model = self
        template_name = "event_detail.html"

        # Pass event to events_detail.html
        return render(request, template_name, {'event': model})
class EventDelete(DeleteView):
    model = Event





