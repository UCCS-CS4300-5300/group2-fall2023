### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Models """

from io import BytesIO
from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Common.forms import ProductImageForm
from Common.services import ImageService


class ProductImageFormTests(TestCase):
    """ Test the ProductImageForm """


    def test_valid_product_image_form(self):
        """ Test valid submission of image upload form """

        valid_image = Image.new("RGB", (
            ImageService.DEFAULT_IMAGE_WIDTH,
            ImageService.DEFAULT_IMAGE_HEIGHT,
        ))

        buffer = BytesIO()
        valid_image.save(buffer, format="JPEG")
        buffer.seek(0)

        valid_image_file = SimpleUploadedFile(
            "test_image.jpg",
            buffer.read(),
            content_type="image/jpeg",
        )

        data = {
            "alt_text": "Test Image",
        }

        files = {
            "file": valid_image_file
        }

        form = ProductImageForm(data=data, files=files)
        self.assertTrue(form.is_valid())


    def test_product_image_form_bad_file(self):
        """ Test the product image form with a bad file """

        bad_file_content = b"Some file content"

        buffer = BytesIO(bad_file_content)
        buffer.seek(0)

        bad_file = SimpleUploadedFile(
            "bad_file.txt",
            buffer.read(),
            content_type="plain/text",
        )

        data = {
            "alt_text": "Bad file",
        }

        files = {
            "file": bad_file,
        }

        form = ProductImageForm(data=data, files=files)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)

    def test_product_image_form_invalid_dimensions(self):
        """ Test the product image form with a invalid image dimensions """

        invalid_image = Image.new("RGB", (
            ImageService.MAX_IMAGE_SIZE[0] + 1,
            ImageService.MAX_IMAGE_SIZE[1] + 1,
        ))

        buffer = BytesIO()
        invalid_image.save(buffer, format="JPEG")
        buffer.seek(0)

        invalid_image_file = SimpleUploadedFile(
            "invalid_image.jpg",
            buffer.read(),
            content_type="image/jpeg",
        )

        data = {
            "alt_text": "Invalid Image",
        }

        files = {
            "file": invalid_image_file
        }

        form = ProductImageForm(data=data, files=files)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
