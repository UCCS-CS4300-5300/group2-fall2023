### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from Events.models import Event
from Events.forms import EventForm
from Events.utils import get_coordinates

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
    """ Get event/market details. URL `/markets/<int:pk>/` """

    model = Event
    template_name = "event_detail.html"

    def get_context_data(self, **kwargs):
        """ Update context data """

        # Note that we are updating the context data with the Google Maps API Key
        #   This means that the key is being passed to the client side data. This is 
        #   crucial in order to implement autocomplete functionality. IT IS IMPERITAVE
        #   that you protect your API_KEY through Google's resources (see README for more).

        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY

        return context


class EventCreate(LoginRequiredMixin, CreateView):
    """ Create View for an Event Object. URL `/markets/new` """

    # Establish model type and form class for use
    model = Event
    form_class = EventForm

    # Establish the target template for use
    template_name = "event_create.html"

    def get_context_data(self, **kwargs):
        """ Update context data """

        # Note that we are updating the context data with the Google Maps API Key
        #   This means that the key is being passed to the client side data. This is 
        #   crucial in order to implement autocomplete functionality. IT IS IMPERITAVE
        #   that you protect your API_KEY through Google's resources (see README for more).

        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY

        return context

    def form_valid(self, form):
        """ Update the latitude and longitude fields using the address """

        coords = get_coordinates(settings.GOOGLE_MAPS_API_KEY, form.instance.location)

        if(coords):
            form.instance.latitude = coords[0]
            form.instance.longitude = coords[1]

        else:

            # TODO better handling for this case
            form.instance.latitude = 0.0
            form.instance.longitude = 0.0

        return super().form_valid(form)


class EventUpdate(LoginRequiredMixin, UpdateView):
    """ Update View for an Event Object. URL `/markets/edit/<int:pk>` """

    # Establish model type and form class for use
    model = Event
    form_class = EventForm

    # Establish the target template for use
    template_name = "event_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'start_time': self.object.start_time,
            'end_time': self.object.end_time
        }
        return kwargs

    def get_context_data(self, **kwargs):
        """ Update context data """

        # Note that we are updating the context data with the Google Maps API Key
        #   This means that the key is being passed to the client side data. This is 
        #   crucial in order to implement autocomplete functionality. IT IS IMPERITAVE
        #   that you protect your API_KEY through Google's resources (see README for more).

        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY

        return context

    def form_valid(self, form):
        """ Update the latitude and longitude fields using the address """

        coords = get_coordinates(settings.GOOGLE_MAPS_API_KEY, form.instance.location)

        if(coords):
            form.instance.latitude = coords[0]
            form.instance.longitude = coords[1]

        else:

            # TODO better handling for this case
            form.instance.latitude = 0.0
            form.instance.longitude = 0.0

        return super().form_valid(form)


class EventDelete(LoginRequiredMixin, DeleteView):
    """ View to delete an Event. URL `/markets/delete/<int:pk>` """

    # Establish the model type and template name for the generic view
    model = Event
    template_name = "event_delete.html"

    # Establish the success url to redirect back to the events homepage
    success_url = reverse_lazy('events')


