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

    def check_end_time_not_before_start_time(self):
        # TODO figure out how to compare datetimes
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")

    def start_time_not_in_past(self):   
        # TODO figure out how to compare datetimes   
        start_time = self.data.get("start_time")




