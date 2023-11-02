### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Views

from django.shortcuts import render, redirect
from .models import Event
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EventForm

class EventList(ListView):
    """ Get a list of Harvestly events. URL `/get-events-list/` """
    
    def get(self, request):
        """ Query all events, render in events list template. """
        # Query events
        model = Event.objects.all()
        template_name = "event_list.html"

        # Pass events to events_list.html
        return render(request, template_name, {'eventlist': model})
    
    def post(self, request):
        form = EventForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            object = form.save(commit=False)
            object.save()
            return redirect('event-list')

class EventDetail(DetailView):
    def detail_event(self, request):
        model = self
        template_name = "event_create.html"

        # Pass event to events_create.html
        return render(request, template_name, {'event': model})
    
class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_create.html"

class EventUpdate(UpdateView):
    def get_event(self, request):
        model = self
        template_name = "event_detail.html"

        # Pass event to events_detail.html
        return render(request, template_name, {'event': model})
class EventDelete(DeleteView):
    model = Event





