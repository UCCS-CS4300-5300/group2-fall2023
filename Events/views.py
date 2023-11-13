### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.shortcuts import render
from .models import Event
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EventForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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


class EventCreate(LoginRequiredMixin, CreateView):
    """ Create View for an Event Object. URL `/markets/new` """

    # Establish model type and form class for use
    model = Event
    form_class = EventForm

    # Establish the target template for use
    template_name = "event_create.html"

    def form_valid(self, form):
        """ Update the `organizer` field after submission """

        form.instance.organizer = self.request.user
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


class EventDelete(LoginRequiredMixin, DeleteView):
    """ View to delete an Event. URL `/markets/delete/<int:pk>` """

    # Establish the model type and template name for the generic view
    model = Event
    template_name = "event_delete.html"

    # Establish the success url to redirect back to the events homepage
    success_url = reverse_lazy('events')


