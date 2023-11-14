from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile

# TODO - [] Migrate image logic from product model
# todo - [] create image model


class Image(models.Model):
    image = models.ImageField()
    thumbnail = models.ImageField()
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.update_image_and_thumbnail()
        super().save(*args, **kwargs)

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
