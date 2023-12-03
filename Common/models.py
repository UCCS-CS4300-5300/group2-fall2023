### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Models

""" Implementation of Common models """

from django.db import models


class ImageUpload(models.Model):
    """ Image upload model """

    file = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        """ ImageUpload meta class implementation """

        abstract = True

    def __str__(self):
        """ Output string representation of model """

        return self.file.name if self.file else "No File"


class ProductImage(ImageUpload):
    """ Product Image model """

    related_model = models.ForeignKey(
        "Products.Product", related_name="image", on_delete=models.CASCADE
    )

    def __str__(self):
        """ Output string representation of model """

        return f"{self.related_model.name} image"
