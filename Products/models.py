### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

""" Implementation of Product Model """

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.conf import settings
from Events.models import Event

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    """ Product model """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100_000.00),
        ]
    )
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100_000),
        ],
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """ String representation of model """

        return str(self.name)

    def get_absolute_url(self):
        """ Absolute URL for the model - Details page """

        return reverse("product-details", args=[str(self.id)])

    def get_reservation_count(self):
        """ Get total count of reservations """

        from Reservations.models import Reservation

        reservations = Reservation.objects.filter(product=self)
        count = sum(reservation.quantity for reservation in reservations)

        return count
