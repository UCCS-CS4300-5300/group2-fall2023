### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Forms

""" Implementation of Events Form """

from datetime import datetime
from django.utils import timezone
from django import forms
from django.conf import settings
from .models import Event

User = settings.AUTH_USER_MODEL

class DateTimeInput(forms.DateInput):
    """ Class to define local datetime input for the form. """
    input_type = "datetime-local"

class EventForm(forms.ModelForm):
    """ Form class for Event Model"""

    class Meta:
        """ Metaclass for Event Form """
        model = Event
        date_time_format = "%Y-%m-%dT%H:%M"

        fields = [
            "name",
            "location",
            "start_time",
            "end_time"
        ]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Event name (max 255 characters)"}),
            "location": forms.TextInput(),
            "start_time": DateTimeInput(format=date_time_format),
            "end_time": DateTimeInput(format=date_time_format)
        }

        labels = {
            "name": "Event Name:",
            "location": "Location:",
            "start_time": "Start Time:",
            "end_time": "End Time:",
        }

        error_messages = {
            "start_time": {
                "invalid": f"Invalid start time format! Use {date_time_format}!",
            },
            "end_time": {
                "invalid": f"Invalid end time format! Use {date_time_format}!",
            },
        }


    def clean(self):
        """
        Ensure that all required fields are included.
        Ensure that start_time comes before end_time.

        Note that this function is called AFTER clean_start_time() and clean_end_time().
        """

        name = self.cleaned_data.get("name")
        location = self.cleaned_data.get("location")
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")

        if not name:
            raise forms.ValidationError("All fields are required! Include a market name!")

        if not location:
            raise forms.ValidationError("All fields are required! Include a market location!")

        if not start_time:
            raise forms.ValidationError("All fields are required! Include a market start time!")

        if not end_time:
            raise forms.ValidationError("All fields are required! Include a market end time!")

        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("End time must come after start time!")

        return self.cleaned_data


    def clean_start_time(self):
        """ Ensure that the start_time is not in the past """

        start_time = self.cleaned_data.get("start_time")
        now = datetime.now(timezone.get_current_timezone())

        start_time_aware = datetime(
            start_time.year,
            start_time.month,
            start_time.day,
            start_time.hour,
            start_time.minute,
            tzinfo=timezone.get_current_timezone()
        )

        # Note, we do not raise an error here
        #   We need to return a value so that 'clean()' knows the field is non-null

        if start_time_aware < now:
            self.add_error("start_time", "Start time must not be in the past!")

        return start_time


    def clean_end_time(self):
        """ Ensure that the end_time is not in the past """

        end_time = self.cleaned_data.get("end_time")
        now = datetime.now(timezone.get_current_timezone())

        end_time_aware = datetime(
            end_time.year,
            end_time.month,
            end_time.day,
            end_time.hour,
            end_time.minute,
            tzinfo=timezone.get_current_timezone()
        )

        # Note, we do not raise an error here
        #   We need to return a value so that 'clean()' knows the field is non-null

        if end_time_aware < now:
            self.add_error("end_time", "End time must not be in the past!")

        return end_time
