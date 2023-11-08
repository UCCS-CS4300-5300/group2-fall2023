### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Events Views

from django.test import TestCase
from django.urls import reverse
from Events.models import Event


class EventListTests(TestCase):
    """ Test the Event List View """
    def test_event_list_at_url(self):
        """ Verify that the event list exists at `/events/` """

        response = self.client.get("/events/")

        self.assertEqual(response.status_code, 200)

    def test_event_list_at_reverse_lookup(self):
        """ Verify that the event list exists with reverse lookup of `events` """

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)

    def test_event_list_uses_template(self):
        """ Verify that the event list uses the correct template """

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed("event_list.html")

    def test_event_list_uses_layout(self):
        """ Verify that the event list uses the layout template """

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("layout.html")

    def test_event_list_empty_uses_empty_template(self):
        """ Test the event list view when no events exist """

        response = self.client.get(reverse("events"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_list.html")
        self.assertTemplateUsed(response, "empty_list.html")

    def test_event_list_with_events(self):
        """ Test the event list view with event objects """
        # TODO this isn't the ideal way to test the feature... check back later
        event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2023-12-01T09:00+03:00",
            end_time = "2023-12-01T10:00+03:00",
        )

        event_2 = Event.objects.create(
            id=2,
            name="Event 2",
            location="Event 2 Location",
            start_time="2023-12-01T11:00+03:00",
            end_time = "2023-12-01T12:00+03:00",
        )

        response = self.client.get(reverse("events"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_list.html")
        self.assertContains(response, event_1.name)
        self.assertContains(response, event_2.name)


class EventDetailTests(TestCase):
    """ Test the Event Detail View """

    def setUp(self):
        """ Create an object to view details """
        
        self.event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2023-12-01T09:00+03:00",
            end_time="2023-12-01T10:00+03:00",
        )

    
    def test_event_detail_at_url(self):
        """ Verify that the event detail exists at `/events/details/<int:pk>` """

        response = self.client.get(f"/events/{self.event_1.id}")

        self.assertEqual(response.status_code, 200)


    def test_event_detail_at_reverse_lookup(self):
        """ Verify that the event detail exists with reverse lookup of `product-details` """

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_event_detail_uses_template(self):
        """ Verify that the event detail view uses the correct template """

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_detail.html")


    def test_event_detail_uses_layout(self):
        """ Verify that the event detail view uses the layout template """

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_event_detail_missing_object(self):
        """ Test the event detail view when there is no object at the given argument """

        response = self.client.get(reverse("event-detail", args=["999"]))

        self.assertEqual(response.status_code, 404)


    def test_pevent_detail_displays_object_details(self):
        """ Test that the event detail view displays event details """

        response = self.client.get(reverse("event-detail", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event_1.name)
        self.assertContains(response, self.event_1.location)


class EventCreateTests(TestCase):
    """ Test the Event Create View """

    # TODO


class EventUpdateTests(TestCase):
    """ Test the Event Update View """

    # TODO


class EventDeleteTests(TestCase):
    """ Test the Event Delete View """

    def setUp(self):
        """ Create an event to be deleted """

        self.event_1 = Event.objects.create(
            id=1,
            name="Event 1",
            location="Event 1 Location",
            start_time="2023-12-01T09:00+03:00",
            end_time="2023-12-01T10:00+03:00",
        )


    def test_event_delete_at_url(self):
        """ Verify that the event delete exists at `/events/<int:pk>/delete/` """

        response = self.client.get(f"/events/{self.event_1.id}/delete")

        self.assertEqual(response.status_code, 200)


    def test_event_delete_at_reverse_lookup(self):
        """ Verify that the product delete exists with reverse lookup of `event-delete` """

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_product_delete_uses_template(self):
        """ Verify that the product delete view uses the correct template """

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_delete.html")


    def test_product_delete_uses_layout(self):
        """ Verify that the product delete view uses the layout template """

        response = self.client.get(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_product_delete_missing_object(self):
        """ Test the product delete view when there is no object at the given argument """

        response = self.client.get(reverse("event-delete", args=["999"]))

        self.assertEqual(response.status_code, 404)

    
    def test_product_delete_valid(self):
        """ Test the product delete post with a valid object ID """

        response = self.client.post(reverse("event-delete", args=[self.event_1.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(id=self.event_1.id).exists())
