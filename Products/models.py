### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

from django.db import models
from Events.models import Event

class Vendor(models.Model):
    """ Vendor model. """

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Product model. """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # image = models.ImageField(upload_to='products/images') # need pillow installed
    product_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
