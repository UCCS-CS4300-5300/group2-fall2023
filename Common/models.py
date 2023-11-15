from django.db import models
from PIL import Image as PILImage
from io import BytesIO
import os
import uuid
from django.core.files.base import ContentFile

# TODO - [x] Migrate image logic from product model
# todo - [x] create image model
# TODO - [] abstraction inherited productImage model.
# TODO - [x] implement image update logic
# TODO - [x] implement unique_filename method
# TODO - [x] implement image validation
# TODO - [] handle alt text for images

MAX_IMAGE_SIZE = (1920, 1920)
DEFAULT_IMAGE_SIZE = (480, 480)
DEFAULT_THUMBNAIL_SIZE = (128, 128)
IMAGE_QUALITY = 85
ACCEPTED_FILE_TYPES = ["JPEG", "JPG", "PNG"]
MIN_FILE_SIZE = 10240  # file size: 10 KB
MAX_FILE_SIZE = 5242880  # file size: 5 MB


class ImageUpload(models.Model):
    file = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.file.name if self.file else "No File"

    def save(self, *args, **kwargs):
        if not self.file:
            old_instance = type(self).objects.get(id=self.id)
            if old_instance.file:
                old_instance.file.delete(save=False)
            if old_instance.thumbnail:
                old_instance.thumbnail.delete(save=False)

        if self.file:
            self.create_image()
            self.create_thumbnail()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # If there's a file associated with this instance, delete it
        # TODO - Deletion still not fully working
        print("deleting image")
        if self.file:
            self.file.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)

        super().delete(*args, **kwargs)

    def create_image(self):
        """Create image from image field"""
        if not self.file:
            return

        # resize main image to create a thumbnail.
        image_size = DEFAULT_IMAGE_SIZE
        resized_image = self.resize_image(self.file, image_size)

        # ensure thumbnail is created, even if it's same size or smaller
        if resized_image is None:
            resized_image = self.file

        # save thumbnail
        image_filename = self.generate_unique_filename(self.file.name)
        self.file = ContentFile(resized_image.read(), image_filename)

    def create_thumbnail(self):
        """Create thumbnail from image field"""
        if not self.file:
            return

        # resize main image to create a thumbnail.
        thumbnail_size = DEFAULT_THUMBNAIL_SIZE
        resized_thumbnail = self.resize_image(self.file, thumbnail_size)

        # ensure thumbnail is created, even if it's same size or smaller
        if resized_thumbnail is None:
            resized_thumnail = self.file

        # save thumbnail
        thumbnail_filename = self.generate_unique_filename(self.file.name)
        self.thumbnail = ContentFile(resized_thumbnail.read(), thumbnail_filename)

    @staticmethod
    def resize_image(image, size, quality=IMAGE_QUALITY):
        """Resize image to fit within the specified size"""
        # check for image
        if not image:
            return None

        print("image exists in resize_image")
        # open image
        img = PILImage.open(image)

        if img.size > size:
            img.thumbnail(size)

        # resize image while maintaining aspect ratio

        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=quality)
        thumb_io.seek(0)

        return thumb_io

    @staticmethod
    def generate_unique_filename(filename):
        """Generate unique filename"""
        file = os.path.basename(filename)
        name, extension = os.path.splitext(file)
        return f"{name}_{uuid.uuid4()}{extension}"

    @staticmethod
    def validate_image_size_parameter(size):
        # Validate the size parameter is a tuple of length 2
        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError("size parameter must be a tuple of (width, height)")
        # validate size elements are positive integers
        if not all(isinstance(n, int) and n > 0 for n in size):
            raise ValueError("size must contain positive integers")

    def delete_old_files():
        pass


class ProductImage(ImageUpload):
    product = models.ForeignKey(
        "Products.Product", related_name="image", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.product.name

    def delete(self, *args, **kwargs):
        # If there's a file associated with this instance, delete it
        print("deleting product image")
        if self.file:
            self.file.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)

        super().delete(*args, **kwargs)
