### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Events Forms


from django.test import TestCase
from Events import forms

# TODO - Update when location field changes

class EventFormTests(TestCase):
    """ Test the Event Form """

    def test_valid_event_form(self):
        """ Test the event form is recognized as valid """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2023-12-01T09:00",
            "end_time": "2023-12-03T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertTrue(form.is_valid())


    def test_event_form_missing_name(self):
        """ Test event form when name is missing """
        
        data = {
            "location": "Some Location",
            "start_time": "2023-12-01T09:00",
            "end_time": "2023-12-03T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


    def test_event_form_missing_location(self):
        """ Test event form when name is missing """
        
        data = {
            "name": "Some Event",
            "start_time": "2023-12-01T09:00",
            "end_time": "2023-12-03T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("location", form.errors)

    
    def test_event_form_missing_start_time(self):
        """ Test event form when start time is missing """
        
        data = {
            "name": "Some Event",
            "location": "Some Location",
            "end_time": "2023-12-03T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_time", form.errors)


    def test_event_form_missing_end_time(self):
        """ Test event form when start time is missing """
        
        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2023-12-01T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_time", form.errors)


    def test_event_form_invalid_start_time(self):
        """ Test the event form when the start time is not in the correct format """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2023-12",
            "end_time": "2023-12-03T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_time", form.errors)


    def test_event_form_invalid_end_time(self):
        """ Test the event form when the end time is not in the correct format """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2023-12-01T09:00",
            "end_time": "T09:00",
        }

        form = forms.EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("end_time", form.errors)

