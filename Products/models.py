### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

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
        return self.name

    def get_absolute_url(self):
        return reverse("product-details", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        for image in self.image.all():
            if image.file:
                image.file.delete(save=False)
            if image.thumbnail:
                image.thumbnail.delete(save=False)
            image.delete()
        super().delete(*args, **kwargs)


class Reservation(models.Model):
    """ Reservation model - Linking table between User and Product """

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )

    price = models.FloatField()