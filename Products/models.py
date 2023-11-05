### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

from django.db import models
from django.core.validators import MinValueValidator
from Events.models import Event


class Product(models.Model):
    """ Product model. """

    # TODO - Install pillow to upload images
    # TODO - Set up vendors app/model to link vendors to users,products,events
    # TODO - Set up link between events and product additions

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )

    # TODO - seee above
    # image = models.ImageField(upload_to='products/images')
    # product_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    product_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
