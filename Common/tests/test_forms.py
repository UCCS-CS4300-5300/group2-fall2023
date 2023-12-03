### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Models """

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Common.forms import ImageUploadForm, ProductImageForm


class ProductImageFormTests(TestCase):
    """ Test the ProductImageForm """

    def setUp(self):
        """ Set up for testing the ImageUploadForm """

        image_content = b"test_image_content"

        self.test_image = SimpleUploadedFile(
            "image_file.jpg",
            image_content,
            content_type="image/jpeg"
        )

    def test_valid_image_upload_form(self):
        """ Test valid submission of image upload form """

        data = {
            "file": self.test_image,
            "alt_text": "Test Image",
        }

        form = ProductImageForm(data=data)
        self.assertTrue(form.is_valid())
