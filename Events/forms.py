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
            'start_time': DateTimeInput(),
            'end_time': DateTimeInput()
        }
