### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Models

from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile

# from Events.models import Event


class Product(models.Model):
    """Product model"""

    # TODO - [x] Install Pillow to work with images
    # TODO - [] tweak image sizing to fit needs.
    # ? currently 480x480 and 128x128 (thumb)
    # TODO - [] Set up vendors app/model to link vendors to users,products,events
    # TODO - [] Set up link between events and products

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )
    # include images for products.
    image = models.ImageField(
        upload_to="products/images",
        blank=True,
        null=True,
    )
    # add thumbnail field for products
    thumbnail = models.ImageField(
        upload_to="products/thumbnails", blank=True, null=True
    )

    # TODO - see above
    # product_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    # product_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.update_image_and_thumbnail()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-details", args=[str(self.id)])

    def update_image_and_thumbnail(self):
        """creates or updates the image and thumbnail for the product"""
        # resize primary image
        resized_image = Product.resize_image(self.image, size=(480, 480))
        if resized_image:
            filename = os.path.basename(self.image.name)
            self.image.name = filename
            self.image.save(self.image.name, resized_image, save=False)

        # update/create thumbnail
        thumbnail_image = Product.resize_image(self.image, size=(128, 128))
        if thumbnail_image:
            # extract filename from image name
            filename = os.path.basename(self.image.name)
            self.thumbnail.name = filename
            self.thumbnail.save(self.thumbnail.name, thumbnail_image, save=False)

    @staticmethod
    def resize_image(image, size=(480, 480)):
        """Resize image to fit within the specified size"""
        # check for image
        if not image:
            return None

        # open image
        img = Image.open(image)
        (width, height) = img.size
        if (width, height) <= size:
            return None

        # resize image while maintaining aspect ratio
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        return ContentFile(thumb_io.getvalue())
