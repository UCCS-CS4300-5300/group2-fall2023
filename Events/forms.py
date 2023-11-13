### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Forms

from datetime import datetime
from django.utils import timezone
from django import forms
from .models import Event

class DateTimeInput(forms.DateInput):
    input_type = "datetime-local"

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "location",
            "start_time",
            "end_time"
        ]
        
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Event name (max 255 characters)"}),
            "location": forms.TextInput(),
            "start_time": DateTimeInput(format="%Y-%m-%dT%H:%M"),
            "end_time": DateTimeInput(format="%Y-%m-%dT%H:%M")
        }

        labels = {
            "name": "Event Name:",
            "location": "Location:",
            "start_time": "Start Time:",
            "end_time": "End Time:",
        }


    def clean_start_time(self):
        """ Ensure that the start_time is not in the past """

        start_time = self.cleaned_data.get("start_time")
        now = datetime.now(timezone.get_current_timezone())

        if start_time:
            start_time_aware = datetime(
                start_time.year,
                start_time.month,
                start_time.day,
                start_time.hour,
                start_time.minute,
                tzinfo=timezone.get_current_timezone()
            )

            if start_time_aware < now:
                raise forms.ValidationError("Start time must not be in the past!")
        
        return start_time
    

    def clean_end_time(self):
        """ Ensure that the start_time comes before end_time """

        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")

        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("End time must come after start time!")
        
        return end_time






