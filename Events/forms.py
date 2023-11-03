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
            'name': forms.TextInput(attrs={'class':'', 'style':'width: 300px; border-radius: 3px;'}),
            'location': forms.TextInput(attrs={'style':'width: 300px; border-radius: 3px;'}),
            'start_time': DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'style':'width: 300px; border-radius: 3px;'}),
            'end_time': DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'style':'width: 300px; border-radius: 3px;'})
        }


