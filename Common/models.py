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
        if self.file:
            print("in image model save method")
            self.update_image_field("file", DEFAULT_IMAGE_SIZE)
            self.update_image_field("thumbnail", DEFAULT_THUMBNAIL_SIZE)
        super().save(*args, **kwargs)

    def update_image_field(self, field_name, size):
        """
        Update image field specified by field_name to the given size
        :param field_name: name of image field to update (image, or thumb)
        :param size: The size in tuple (width, height) to rezise the img to.
        """
        # validate size paramater is a tuple
        self.validate_image_size_parameter(size)

        # get image field
        image_field = getattr(self, field_name)
        # save current file path to delete later if it's updated
        old_file_path = (
            image_field.path
            if image_field and os.path.isfile(image_field.path)
            else None
        )

        # resize image to fit within the specified size
        resized_image = self.resize_image(image_field, size)

        # if resized image exists, create new file and set image field to it
        if resized_image:
            filename = self.generate_unique_filename(image_field.name)
            new_file = ContentFile(resized_image.getvalue(), filename)
            setattr(self, field_name, new_file)

            # TODO - refactor to generic delete file method
            if old_file_path:
                # delete old file
                os.remove(old_file_path)

    

    @staticmethod
    def resize_image(image, size):
        """Resize image to fit within the specified size"""
        print("in resize image method")
        # check for image
        if not image:
            return None

        print("image exists in resize_image")
        # open image
        img = PILImage.open(image)
        thumb_io = BytesIO()

        if img.size <= size:
            return img.save(thumb_io, img.format, quality=IMAGE_QUALITY)

        print("image is larger than size")

        # resize image while maintaining aspect ratio
        img.thumbnail(size)
        img.save(thumb_io, img.format, quality=IMAGE_QUALITY)

        return thumb_io

    @staticmethod
    def generate_unique_filename(filename):
        """Generate unique filename"""
        name, extension = os.path.splitext(filename)
        return f"{name}_{uuid.uuid4()}{extension}"

    @staticmethod
    def validate_image_size_parameter(size):
        # Validate the size parameter is a tuple of length 2
        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError("size parameter must be a tuple of (width, height)")
        # validate size elements are positive integers
        if not all(isinstance(n, int) and n > 0 for n in size):
            raise ValueError("size must contain positive integers")


class ProductImage(ImageUpload):
    product = models.ForeignKey(
        "Products.Product", related_name="image", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.product.name
