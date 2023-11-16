import os, uuid
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# !! LEAVE THIS IMPORT HERE FOR NOW
from .models import ProductImage


class ImageService:
    # macros
    MAX_IMAGE_SIZE = (1920, 1920)
    DEFAULT_IMAGE_WIDTH = 480
    DEFAULT_IMAGE_HEIGHT = 480
    DEFAULT_IMAGE_SIZE = (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT)
    DEFAULT_THUMBNAIL_SIZE = (128, 128)
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
        """
        Saves an image, resizing if necessary, and associates with a model instance.
        """

        if resize_to:
            image_file = self._resize_image(image_file, resize_to)

        if alt_text is None:
            alt_text = self.generate_alt_text(related_object)

        # generate a unique filename
        filename = self._generate_unique_filename(image_file.name)
        path = os.path.join("images", filename)

        # save image file
        saved_path = default_storage.save(path, ContentFile(image_file.read()))

        thumbnail = self.create_thumbnail(image_file)

        # create Image model instance
        image_instance = image_model(
            file=saved_path,
            alt_text=alt_text,
            thumbnail=thumbnail,
            related_object=related_object,
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
        """
        Updates an image, resizing if necessary.
        """

        if resize_to:
            new_image_file = self._resize_image(new_image_file, resize_to)

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

    def delete_image(self, image_instance):
        """Deletes an image model instance and its associated files."""
        if image_instance.file:
            image_instance.file.delete(save=False)
        if image_instance.thumbnail:
            image_instance.thumbnail.delete(save=False)
        image_instance.delete()

    def handle_image_update(
        self, cleaned_data, related_object, image_model, resize_to=None
    ):
        new_file = cleaned_data.get("file")
        new_alt_text = cleaned_data.get("alt_text")
        clear_image = cleaned_data.get("clear")

        existing_image_instance = related_object.image.first()

        if new_file is None and clear_image:
            if existing_image_instance:
                self.delete_image(existing_image_instance)
        elif new_file:
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
        """
        img = PILImage.open(image_file)
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, img.format)
        thumb_io.seek(0)

        return ContentFile(thumb_io.read(), name=image_file.name)

    def generate_alt_text(self, related_object):
        return f"{related_object.name} image"

    def _resize_image(self, image_file, size=DEFAULT_IMAGE_SIZE):
        """
        Resizes an image to the specified size.
        """
        img = PILImage.open(image_file)
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, img.format)
        thumb_io.seek(0)

        return ContentFile(thumb_io.read(), name=image_file.name)

    def _generate_unique_filename(self, filename):
        """
        Generates a unique filename.
        """
        name, extension = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4()}{extension}"
        return unique_filename
