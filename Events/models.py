### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Models

""" Implementation of Event Model """

from django.db import models
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    """ Class for Event Model """

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_products(self):
        """ Query the `Product` model to get all products associated with this event """
        from Products.models import Product  # import goes here to avoid a circular import error
        return Product.objects.filter(product_event=self.id)

    def get_absolute_url(self):
        """ Get the absolute url of the Event Object """
        return reverse("event-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Ensure that latitude and longitude are set before calling super().save()
        if self.latitude is None:
            self.latitude = 0.0
        if self.longitude is None:
            self.longitude = 0.0

        # call clean() before saving
        self.full_clean()
        super().save(*args, **kwargs)
