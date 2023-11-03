from django import forms
from .models import Event

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
            'start_time': forms.DateTimeInput(),
            'end_time': forms.DateTimeInput()
        }