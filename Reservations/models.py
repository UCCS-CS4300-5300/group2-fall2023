### CS 4300 Fall 2023 Group 2
### Harvestly
### Reservation Models

""" Implementation of Reservation Model """

from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from Products.models import Product

User = settings.AUTH_USER_MODEL

class Reservation(models.Model):
    """ Reservation model - Linking table between User and Product """

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    price = models.FloatField()
