### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.shortcuts import render
from .models import Event
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EventForm
from django.urls import reverse_lazy

class EventList(ListView):
    """ Get a list of Harvestly events. URL `/event-list/` """

    def get(self, request):
        """ Query all events, render in events list template. """
        
        # Query events
        model = Event.objects.all()
        template_name = "event_list.html"

        # Pass events to events_list.html
        return render(request, template_name, {'eventlist': model})


class EventDetail(DetailView):
    """ Get event/market details. URL `/events/<int:pk>/` """

    model = Event
    template_name = "event_detail.html"


class EventCreate(CreateView):
    """ Create View for an Event Object. URL `/events/new` """

    # Establish model type and form class for use
    model = Event
    form_class = EventForm

    # Establish the target template for use
    template_name = "event_create.html"


class EventUpdate(UpdateView):
    """ Update View for an Event Object. URL `/events/<int:pk>/update` """

    # Establish model type and form class for use
    model = Event
    form_class = EventForm

    # Establish the target template for use
    template_name = "event_update.html"


class EventDelete(DeleteView):
    """ View to delete an Event. URL `/events/<int:pk>/delete` """

    # Establish the model type and template name for the generic view
    model = Event
    template_name = "event_delete.html"

    # Establish the success url to redirect back to the events homepage
    success_url = reverse_lazy('events')


