from django import forms
from .models import Event

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'location',
            'start_time',
            'end_time'
        ]
        
        widgets = {
            'name': forms.TextInput(),
            'location': forms.TextInput(),
            'start_time': DateTimeInput(format='%Y-%m-%dT%H:%M'),
            'end_time': DateTimeInput(format='%Y-%m-%dT%H:%M')
        }

        labels = {
            "name": "Event Name:",
            "location": "Location:",
            "start_time": "Start Time:",
            "end_time": "End Time:",
        }


