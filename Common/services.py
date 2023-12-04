### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Services

""" Implementation of Common models """

import os
import uuid
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class ImageService:
    """Image Service"""

    # macros
    MAX_IMAGE_SIZE = (1920, 1920)
    DEFAULT_IMAGE_WIDTH = 1080
    DEFAULT_IMAGE_HEIGHT = 720
    DEFAULT_IMAGE_SIZE = (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT)
    DEFAULT_THUMBNAIL_SIZE = (640, 480)
    IMAGE_QUALITY = 85
    ACCEPTED_FILE_TYPES = ["JPEG", "JPG", "PNG"]
    MIN_FILE_SIZE = 10240  # file size: 10 KB
    MAX_FILE_SIZE = 5242880  # file size: 5 MB
    MIN_FILE_SIZE_KB = MIN_FILE_SIZE / 1024
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE / 1024 / 1024

    def create_image(
        self,
        image_file,
        related_object,
        image_model,
        alt_text=None,
        resize_to=DEFAULT_IMAGE_SIZE,
    ):
        """Create a new image object

        Args:
            image_file (file): an image file
            related_object (object): the object type being related to image.
            image_model (ImageUpload object): The specific object model inheriting ImageUpload.
            alt_text (string, optional): an image's descriptive alternative text. Defaults to None.
            resize_to (int tuple, optional): (width, height). Defaults to DEFAULT_IMAGE_SIZE.

        Returns:
            image_instance: returns the newly created image instance.
        """

        if resize_to:
            image_file = self.resize_image(image_file, resize_to)
        if alt_text is None:
            alt_text = self.generate_alt_text(related_object)

        # generate unique filename
        filename = self.generate_unique_filename(image_file.name)
        # set model name
        model_name = related_object.__class__.__name__.lower()
        # create file path
        file_path = os.path.join(model_name, "images", filename)
        # save image
        saved_path = default_storage.save(
            file_path,
            ContentFile(image_file.read())
        )
        # thumb path
        thumb_path = os.path.join(model_name, "thumbnails", f"thumb_{filename}")
        # create thumbnail
        thumbnail = self.create_thumbnail(image_file, thumb_path)


        # create Image model instance
        image_instance = image_model(
            file=saved_path,
            alt_text=alt_text,
            thumbnail=thumbnail,
            related_model=related_object,
        )
        image_instance.save()

        return image_instance

    def handle_image_update(self, image_form, related_object, image_model):
        """
        helper method for image update process, re-routes to update or create image.

        Args:
            image_form (ImageUploadForm): form containing image data
            related_object (model instance): object related to image
            image_model (ImageUplaod object): intermediary model relates image w/ related_object
            resize_to (integer tuple, optional): (height, width). Defaults to None.
        """

        # check if file field was changed
        if 'file' not in image_form.changed_data:
            return

        new_file = image_form.cleaned_data.get("file")
        new_alt_text = image_form.cleaned_data.get("alt_text")

        existing_image_instance = related_object.image.first()


        # file field changed, delete existing image instance
        if existing_image_instance:
            existing_image_instance.delete()

        # create new image instance
        if new_file:
            self.create_image(
                new_file,
                related_object,
                image_model,
                alt_text=new_alt_text,
            )

    def create_thumbnail(self, image_file, thumb_path, size=DEFAULT_THUMBNAIL_SIZE):
        """
        Resizes an image to the specified size.
        :param image_file: an image file (img.png, img.jpg)
        :param size: integer tuple (height, width)
        """
        with PILImage.open(image_file) as img:
            img.thumbnail(size)

            thumb_io = BytesIO()
            img_format = img.format if img.format else "JPEG"
            img.save(thumb_io, img_format, quality=self.IMAGE_QUALITY)
            thumb_io.seek(0)

            # save thumbnail and return
            thumbnail = default_storage.save(
                thumb_path,
                ContentFile(thumb_io.getvalue())
            )

            return thumbnail

    def generate_alt_text(self, related_object):
        """
        generates alt text based upon the image's related object
        :param related_object: object with relation to image object
        """
        return f"{related_object.name} image"

    def resize_image(self, image_file, size=DEFAULT_IMAGE_SIZE):
        """
        Resizes an image to the specified size.
        :param image_file: a file
        :param size: tuple (width, height) for resizing img
        """
        with PILImage.open(image_file) as img:
            img.thumbnail(size)

            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            thumb_io.seek(0)

            return ContentFile(thumb_io.read(), name=image_file.name)

    def generate_unique_filename(self, filename):
        """
        Generates a unique filename.
        :param filename: name of a file
        e.g. file.png
        """

        name, extension = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4()}{extension}"
        return unique_filename
