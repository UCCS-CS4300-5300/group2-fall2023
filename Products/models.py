### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.conf import settings
from Events.models import Event

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    """Product model"""

    # TODO - Set up vendors app/model to link vendors to users,products,events

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, blank=True, null=True
    )

    # TODO - see above
    # product_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    # product_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-details", args=[str(self.id)])
