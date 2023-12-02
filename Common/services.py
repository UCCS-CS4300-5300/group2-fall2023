### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Services

""" Implementation of Common models """

import os, uuid
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# !! LEAVE THIS IMPORT HERE FOR NOW
from .models import ProductImage

# TODO - [] Add more error checking, especially for PIL and file handling.
# TODO - [] async image resizing
# TODO - [] async image uploading
# TODO - [] async image deletion
# TODO - [] implement image processing method?
# TODO - [] standardize names, design naming scheme
# TODO - [] Work on multiple images logic


class ImageService:
    """ Image Service """

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
            image_model (ImageUpload object): The specific object model inheriting ImageUpload base model.
            alt_text (string, optional): an image's descriptive alternative text. Defaults to None.
            resize_to (int tuple, optional): (width, height). Defaults to DEFAULT_IMAGE_SIZE.

        Returns:
            image_instance: returns the newly created image instance.
        """

        if resize_to:
            image_file = self._resize_image(image_file, resize_to)

        if alt_text is None:
            alt_text = self.generate_alt_text(related_object)

        # generate a unique filename
        filename = self._generate_unique_filename(image_file.name)
        # join the image path to file name
        path = os.path.join("images", filename)

        # save image to content file
        saved_path = default_storage.save(path, ContentFile(image_file.read()))

        thumbnail = self.create_thumbnail(image_file)

        # create Image model instance
        image_instance = image_model(
            file=saved_path,
            alt_text=alt_text,
            thumbnail=thumbnail,
            related_model=related_object,
        )
        image_instance.save()

        return image_instance

    def update_image(
        self,
        image_instance,
        new_image_file,
        alt_text=None,
        resize_to=DEFAULT_IMAGE_SIZE,
    ):
        """Updates an image instance's data.

        Args:
            image_instance (image object): instance of an image model
            new_image_file (file): new file to update image instance to.
            alt_text (string, optional): an image's descriptive alt text. Defaults to None.
            resize_to (int tuple, optional): (width, height). Defaults to DEFAULT_IMAGE_SIZE.

        Returns:
            image_instance: returns the updated image instance.
        """

        if resize_to:
            new_image_file = self._resize_image(new_image_file, resize_to)

        # generate default alt_text if none provided.
        if alt_text is None:
            alt_text = self.generate_alt_text(image_instance.related_object)

        # delete old image file
        if image_instance.file:
            image_instance.file.delete(save=False)

        # generate a new filename for new image
        filename = self._generate_unique_filename(new_image_file.name)
        path = os.path.join("images", filename)

        # save new image file
        saved_path = default_storage.save(path, ContentFile(new_image_file.read()))

        thumbnail = self.create_thumbnail(new_image_file)

        # update image instance with new file path
        image_instance.file = saved_path
        image_instance.alt_text = alt_text
        image_instance.thumbnail = thumbnail
        image_instance.save()

        return image_instance

    def delete_image_files(self, image_instance):
        """Deletes an image instance's associated files from system storage."""
        if image_instance.file:
            image_instance.file.delete(save=False)
        if image_instance.thumbnail:
            image_instance.thumbnail.delete(save=False)

    def delete_image_instance(self, image_instance):
        """deletes an instance of an image, and its associated files if any"""
        self.delete_image_files(image_instance)
        if image_instance:
            image_instance.delete()

    def handle_image_update(
        self, cleaned_data, related_object, image_model, resize_to=None
    ):
        """helper method for image update process, re-routes to update or create image.

        Args:
            cleaned_data (object): cleaned data returned from image form
            related_object (model instance): object related to image
            image_model (the intermediary model to relate image with related_object): Image data structure
            resize_to (integer tuple, optional): (height, width). Defaults to None.
        """
        new_file = cleaned_data.get("file")
        new_alt_text = cleaned_data.get("alt_text")

        existing_image_instance = related_object.image.first()

        # TODO - clean this structure up a bit

        if not new_file or new_file is None:
            return

        if existing_image_instance:
            self.update_image(
                existing_image_instance,
                new_file,
                alt_text=new_alt_text,
            )
        else:
            self.create_image(
                new_file,
                related_object,
                image_model,
                alt_text=new_alt_text,
            )

    def create_thumbnail(self, image_file, size=DEFAULT_THUMBNAIL_SIZE):
        """
        Resizes an image to the specified size.
        :param image_file: an image file (img.png, img.jpg)
        :param size: integer tuple (height, width)
        """
        with PILImage.open(image_file) as img:
            img.thumbnail(size)

            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            thumb_io.seek(0)

            # generate a unique filename
            filename = f"thumb_{self._generate_unique_filename(image_file.name)}"
            # join the image path to file name
            path = os.path.join("thumbnails", filename)

            # save image to content file
            saved_path = default_storage.save(path, ContentFile(image_file.read()))

            return ContentFile(thumb_io.read(), name=image_file.name)

    def generate_alt_text(self, related_object):
        """
        generates alt text based upon the image's related object
        :param related_object: object with relation to image object
        """
        return f"{related_object.name} image"

    def _resize_image(self, image_file, size=DEFAULT_IMAGE_SIZE):
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

    def _generate_unique_filename(self, filename):
        """
        Generates a unique filename.
        :param filename: name of a file
        e.g. file.png
        """
        name, extension = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4()}{extension}"
        return unique_filename

    def get_image_instance_from_related_obj(
        self, related_object_instance, related_name
    ):
        """
        Returns related instance held by another object instance if it exists.
        :param related_object: instance of an object we are searching for FK
        :param related_name: the related_name field in the related_object_instance
        """
        return related_object_instance.related_name.first() or None
