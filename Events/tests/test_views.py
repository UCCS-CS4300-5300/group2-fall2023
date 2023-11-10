### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Events Views

from django.test import TestCase
from django.urls import reverse
from Events.models import Event
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class EventListTests(TestCase):
    """Test the Event List View"""

    def test_event_list_at_url(self):
        """Verify that the event list exists at `/markets/`"""

        response = self.client.get("/markets/")

        self.assertEqual(response.status_code, 200)

    def test_event_list_at_reverse_lookup(self):
        """Verify that the event list exists with reverse lookup of `events`"""

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)

    def test_event_list_uses_template(self):
        """Verify that the event list uses the correct template"""

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed("event_list.html")

    def test_event_list_uses_layout(self):
        """Verify that the event list uses the layout template"""

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("layout.html")

    def test_event_list_empty_uses_empty_template(self):
        """Test the event list view when no events exist"""

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_list.html")
        self.assertTemplateUsed(response, "empty_list.html")

    def test_event_list_with_events(self):
        """Test the event list view with event objects"""
        # TODO this isn't the ideal way to test the feature... check back later
        event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2024-12-01T09:00+03:00",
            end_time="2024-12-01T10:00+03:00",
        )

        event_2 = Event.objects.create(
            id=2,
            name="Event 2",
            location="Event 2 Location",
            start_time="2024-12-01T11:00+03:00",
            end_time="2024-12-01T12:00+03:00",
        )

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_list.html")
        self.assertContains(response, event_1.name)
        self.assertContains(response, event_2.name)


class EventDetailTests(TestCase):
    """Test the Event Detail View"""

    def setUp(self):
        """Create an object to view details"""

        self.event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2024-12-01T09:00+03:00",
            end_time="2024-12-01T10:00+03:00",
        )

    def test_event_detail_at_url(self):
        """Verify that the event detail exists at `/markets/details/<int:pk>`"""

        response = self.client.get(f"/markets/details/{self.event_1.id}")

        self.assertEqual(response.status_code, 200)

    def test_event_detail_at_reverse_lookup(self):
        """Verify that the event detail exists with reverse lookup of `event-detail`"""

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)

    def test_event_detail_uses_template(self):
        """Verify that the event detail view uses the correct template"""

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_detail.html")

    def test_event_detail_uses_layout(self):
        """Verify that the event detail view uses the layout template"""

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")

    def test_event_detail_missing_object(self):
        """Test the event detail view when there is no object at the given argument"""

        response = self.client.get(reverse("event-detail", args=["999"]))

        self.assertEqual(response.status_code, 404)

    def test_pevent_detail_displays_object_details(self):
        """Test that the event detail view displays event details"""

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event_1.name)
        self.assertContains(response, self.event_1.location)


class EventCreateTests(TestCase):
    """Test the Event Create View"""

    def setUp(self):
        """ Login as user to handle LoginRequired """

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

    def test_event_create_at_url(self):
        """ Verify that the event create exists at `/markets/new` """

        response = self.client.get("/markets/new")

        self.assertEqual(response.status_code, 200)


    def test_event_create_at_reverse_lookup(self):
        """ Verify that the event create exists with reverse lookup of `event-create` """

        response = self.client.get(reverse("event-create"))

        self.assertEqual(response.status_code, 200)


    def test_product_event_uses_template(self):
        """ Verify that the event create view uses the correct template """

        response = self.client.get(reverse("event-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_create.html")


    def test_event_create_uses_layout(self):
        """ Verify that the event create view uses the layout template """

        response = self.client.get(reverse("event-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")

    
    def test_event_creates_object(self):
        """ Verify that the event create view successfully creates an event """

        event_name = "Market 1" 
        data = {
            "name": event_name,
            "location": "Some Location",
            "start_time": "2024-12-01T09:00",
            "end_time": "2024-12-03T09:00",
        }

        response = self.client.post(reverse("event-create"), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name=event_name).exists())


    def test_event_create_missing_name(self):
        """ Test event create view when name is missing """
        
        data = {
            "location": "Some Location",
            "start_time": "2024-12-01T09:00",
            "end_time": "2024-12-03T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_event_create_missing_location(self):
        """ Test event create view when location is missing """
        
        data = {
            "name": "Market 1",
            "start_time": "2024-12-01T09:00",
            "end_time": "2024-12-03T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")

    
    def test_event_create_missing_start_time(self):
        """ Test event create view when start time is missing """
        
        data = {
            "name": "Some Event",
            "location": "Some Location",
            "end_time": "2024-12-03T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_event_create_missing_end_time(self):
        """ Test event create view when end time is missing """
        
        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2024-12-01T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_event_create_invalid_start_time(self):
        """ Test the event create when the start time is not in the correct format """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2024-12",
            "end_time": "2024-12-03T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_event_create_invalid_end_time(self):
        """ Test the event create view when the end time is not in the correct format """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2024-12-01T09:00",
            "end_time": "T09:00",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")

    
    def test_event_create_end_time_before_start_time(self):
        """ Test the event create view when the end time is before the start time """

        data = {
            "name": "Some Event",
            "location": "Some Location",
            "start_time": "2024-12-01T09:00",
            "end_time": "2024-12-01T08:59",
        }

        response = self.client.post(reverse("event-create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")
        self.assertContains(response, "End time must come after start time!")


class EventUpdateTests(TestCase):
    """Test the Event Update View"""

    def setUp(self):
        """ Login as user to handle LoginRequired and Create event object for updating"""

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

        self.event_1 = Event.objects.create(
            name="Event 1",
            location="Event 1 Location",
            start_time=timezone.make_aware(
                datetime.datetime(2025, 11, 1, 10, 0)
            ),  # 2025-11-01 10:00
            end_time=timezone.make_aware(datetime.datetime(2025, 11, 1, 12, 0)),
        )
        self.update_url = reverse("event-update", kwargs={"pk": self.event_1.pk})
        self.res = self.client.get(self.update_url)

    def test_event_update_at_url(self):
        res = self.client.get(f"/markets/edit/{self.event_1.id}")
        self.assertEqual(res.status_code, 200)

    def test_event_update_at_reverse_lookup(self):
        self.assertEqual(self.res.status_code, 200)

    def test_event_update_uses_template(self):
        self.assertEqual(self.res.status_code, 200)
        self.assertTemplateUsed(self.res, "event_update.html")

    def test_event_update_uses_layout(self):
        self.assertEqual(self.res.status_code, 200)
        self.assertTemplateUsed(self.res, "layout.html")

    def test_event_update_missing_object(self):
        bad_res = self.client.get(reverse("event-update", args=["999"]))
        self.assertEqual(bad_res.status_code, 404)

    def test_event_update_displays_object_details(self):
        self.assertEqual(self.res.status_code, 200)

        # get form from context
        form = self.res.context["form"]

        # check initial data is correct
        self.assertEqual(form.initial["name"], self.event_1.name)
        self.assertEqual(form.initial["location"], self.event_1.location)
        self.assertEqual(form.initial["start_time"], self.event_1.start_time)
        self.assertEqual(form.initial["end_time"], self.event_1.end_time)

    def test_event_update_change_name(self):
        new_name = "New Name"
        data = {
            "name": new_name,
            "location": self.event_1.location,
            "start_time": self.event_1.start_time,
            "end_time": self.event_1.end_time,
        }

        updated_res = self.client.post(self.update_url, data=data)
        self.assertEqual(updated_res.status_code, 302)

        updated_event = Event.objects.get(pk=self.event_1.pk)
        self.assertEqual(updated_event.name, new_name)

    def test_event_update_change_location(self):
        new_location = "New Location"
        data = {
            "name": self.event_1.name,
            "location": new_location,
            "start_time": self.event_1.start_time,
            "end_time": self.event_1.end_time,
        }

        updated_res = self.client.post(self.update_url, data=data)
        self.assertEqual(updated_res.status_code, 302)

        updated_event = Event.objects.get(pk=self.event_1.pk)
        self.assertEqual(updated_event.location, new_location)

    def test_event_update_change_start_time(self):
        new_start_time = timezone.make_aware(datetime.datetime(2025, 10, 5, 10, 0))
        data = {
            "name": self.event_1.name,
            "location": self.event_1.location,
            "start_time": new_start_time,
            "end_time": self.event_1.end_time,
        }

        updated_res = self.client.post(self.update_url, data=data)
        self.assertEqual(updated_res.status_code, 302)

        updated_event = Event.objects.get(pk=self.event_1.pk)
        self.assertEqual(updated_event.start_time, new_start_time)

    def test_event_update_change_end_time(self):
        new_end_time = timezone.make_aware(datetime.datetime(2025, 12, 5, 12, 0))

        data = {
            "name": self.event_1.name,
            "location": self.event_1.location,
            "start_time": self.event_1.start_time,
            "end_time": new_end_time,
        }

        updated_res = self.client.post(self.update_url, data=data)
        self.assertEqual(updated_res.status_code, 302)

        updated_event = Event.objects.get(pk=self.event_1.pk)
        self.assertEqual(updated_event.end_time, new_end_time)



class EventDeleteTests(TestCase):
    """Test the Event Delete View"""

    def setUp(self):
        """Login as user to handle LoginRequired and Create an event to be deleted"""

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

        self.event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2024-12-01T09:00+03:00",
            end_time="2024-12-01T10:00+03:00",
        )

    def test_event_delete_at_url(self):
        """Verify that the event delete exists at `/markets/delete/<int:pk>/`"""

        response = self.client.get(f"/markets/delete/{self.event_1.id}")

        self.assertEqual(response.status_code, 200)

    def test_event_delete_at_reverse_lookup(self):
        """Verify that the product delete exists with reverse lookup of `event-delete`"""

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)

    def test_product_delete_uses_template(self):
        """Verify that the product delete view uses the correct template"""

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_delete.html")

    def test_product_delete_uses_layout(self):
        """Verify that the product delete view uses the layout template"""

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")

    def test_product_delete_missing_object(self):
        """Test the product delete view when there is no object at the given argument"""

        response = self.client.get(reverse("event-delete", args=["999"]))

        self.assertEqual(response.status_code, 404)

    def test_product_delete_valid(self):
        """Test the product delete post with a valid object ID"""

        response = self.client.post(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(id=self.event_1.id).exists())
