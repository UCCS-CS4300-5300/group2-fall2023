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
        # check if image is updated/changed before creating new thumbnail.

        if self.image:
            resized_image = Product.resize_image(self.image, size=(480, 480))
            if resized_image:
                self.image.save(self.image.name, resized_image, save=False)

        # create thumbnail if image is updated/changed
        if self.image and not self.thumbnail:
            thumbnail_image = Product.resize_image(self.image, size=(128, 128))
            if thumbnail_image:
                # extract filename from image name
                filename = os.path.basename(self.image.name)
                self.thumbnail.save(f"thumb_{filename}", thumbnail_image, save=False)

        super().save(*args, **kwargs)

    @staticmethod
    def resize_image(image, size=(480, 480)):
        """Resize image to fit within the specified size"""

        if not image:
            return None

        img = Image.open(image)
        original_size = img.size

        # return original image if it is smaller than the specified size
        if original_size[0] <= size[0] and original_size[1] <= size[1]:
            return image

        # resize image while maintaining aspect ratio
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        return ContentFile(thumb_io.getvalue())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-details", args=[str(self.id)])
