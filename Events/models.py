### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Models

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_products(self):
        """ Query the `Product` model to get all products associated with this event """

        from Products.models import Product # import goes here to avoid a cirular import error

        return Product.objects.filter(product_event=self.id)


    def get_absolute_url(self):
        return reverse("event-detail", args=[str(self.id)])

    def clean(self):
        # don't allow end_time to be before start_time
        if self.start_time and self.end_time and self.end_time < self.start_time:
            raise ValidationError("End time cannot be before start time")

    def save(self, *args, **kwargs):
        # call clean() before saving
        self.full_clean()
        super().save(*args, **kwargs)
