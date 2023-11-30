
# CS 4300 Fall 2023 Group 2
# Harvestly
# Test Events Models

""" Test Suite for Event App Models """

import datetime
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from Events.models import Event

class EventTests(TestCase):
    """Test the Event model"""

    def setUp(self):
        """Sets up the data for the test cases"""

        self.user = User.objects.create_user(username="testinguser", password="testingpassword")
        self.user.save()

        self.event = Event.objects.create(
            name="Test Event",
            location="Test Location",
            start_time=timezone.make_aware(
                datetime.datetime(2023, 11, 1, 10, 0)
            ),  # 2023-11-01 10:00
            end_time=timezone.make_aware(
                datetime.datetime(2023, 11, 1, 12, 0)
            ),  # 2023-11-01 12:00
            organizer=self.user,
        )

    def test_event_creation(self):
        """Test valid event creation by testing setUpTestData event creation"""

        event = self.event
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.location, "Test Location")
        self.assertEqual(
            event.start_time, timezone.make_aware(datetime.datetime(2023, 11, 1, 10, 0))
        )  # 2023-11-01 10:00
        self.assertEqual(
            event.end_time, timezone.make_aware(datetime.datetime(2023, 11, 1, 12, 0))
        )  # 2023-11-01 12:00

    def test_field_max_length(self):
        """Test that model has max length attributes set correctly"""

        event = self.event
        name_max_length = event._meta.get_field("name").max_length
        location_max_length = event._meta.get_field("location").max_length

        self.assertEqual(name_max_length, 200)
        self.assertEqual(location_max_length, 255)

    def test_get_absolute_url(self):
        """Test that get_absolute_url returns the correct url"""

        event = self.event
        expected_url = reverse("event-detail", args=[event.pk])
        self.assertEqual(event.get_absolute_url(), expected_url)

    def test_event_time_validation(self):
        """Event end_time cannot be before start_time"""

        event = Event(
            name="Test Event 2",
            location="Test Location 2",
            start_time=timezone.now(),
            end_time=timezone.now()
            - datetime.timedelta(hours=1),  # set end time to 1 hour before start time
        )
        # expect ValidationError since end_time is before start_time
        with self.assertRaises(ValidationError):
            event.full_clean()
