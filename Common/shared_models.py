from django.db import models
from PIL import Image as PILImage
from io import BytesIO
import os
import uuid
from django.core.files.base import ContentFile

# TODO - [x] Migrate image logic from product model
# todo - [x] create image model
# TODO - [] abstraction inherited productImage model.
# TODO - [] implement image update logic
# TODO - [] implement unique_filename method
# TODO - [] implement image validation


class Image(models.Model):
    # Constant values - possibly refactor later
    MAX_IMAGE_SIZE = (480, 480)
    MAX_THUMBNAIL_SIZE = (128, 128)
    IMAGE_QUALITY = 85

    image = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    # product = models.ForeignKey("Products.Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.alt_text

    def save(self, *args, **kwargs):
        # resize image
        # create thumbnail
        # save image
        # generate alt_text
        if self.image:
            self.update_image_field("image", self.MAX_IMAGE_SIZE)
            self.update_image_field("thumbnail", self.MAX_THUMBNAIL_SIZE)
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

            if old_file_path:
                # delete old file
                os.remove(old_file_path)

    @staticmethod
    def resize_image(image, size):
        """Resize image to fit within the specified size"""
        # check for image
        if not image:
            return None

        # open image
        img = PILImage.open(image)
        if img.size <= size:
            return None

        # resize image while maintaining aspect ratio
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=Image.IMAGE_QUALITY)

        return thumb_io

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

    # def update_image_field(self, field_name, size):
    #     """creates or updates the image and thumbnail for the product"""
    #     self.validate_image_size_parameter(size)

    #     image_field = getattr(self, field_name)
    #     # resize primary image
    #     resized_image = Image.resize_image(image_field, size)
    #     if resized_image:
    #         filename = os.path.basename(image_field.name)
    #         # TODO - generate unique filename
    #         new_file = ContentFile(resized_image.getvalue(), filename)
    #         setattr(self, field_name, new_file)
