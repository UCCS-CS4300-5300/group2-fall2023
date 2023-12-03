### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Utilities Methods """

from PIL import Image
from io import BytesIO
from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile

from Common.services import ImageService
from Common.utils import validate_file, \
    validate_image_dimensions, \
    validate_file_size

class UtilsTests(TestCase):
    """ Test the Utils Methods """

    def setUp(self):
        """ Set up testing for utilities methods """

        valid_image = Image.new("RGB", (
            ImageService.DEFAULT_IMAGE_WIDTH,
            ImageService.DEFAULT_IMAGE_HEIGHT,
        ))

        buffer = BytesIO()
        valid_image.save(buffer, format="JPEG")

        self.valid_image_file = InMemoryUploadedFile(
            buffer,
            field_name=None,
            name="test_image.jpg",
            content_type="image/jpeg",
            size=buffer.tell(),
            charset=None,
        )

    def test_successful_validate_file(self):
        """ Test validate file with valid image file """

        self.assertEqual(
            validate_file(self.valid_image_file),
            (True, None)
        )

    def test_successful_validate_image_dimensions(self):
        """ Test validate image dimensions with valid image file """

        self.assertEqual(
            validate_image_dimensions(self.valid_image_file),
            (True, None)
        )

    def test_successful_validate_file_size(self):
        """ Test validate file size with valid image file """

        self.assertEqual(
            validate_file_size(self.valid_image_file),
            (True, None)
        )

    def test_validate_file_bad_file(self):
        """ Test validate file with invalid image file """

        bad_file_content = b"Some file content"
        bad_file_buffer = BytesIO(bad_file_content)

        bad_file = InMemoryUploadedFile(
            bad_file_buffer,
            field_name=None,
            name="bad_file.txt",
            content_type="text/plain",
            size=bad_file_buffer.tell(),
            charset=None,
        )

        self.assertEqual(
            validate_file(bad_file),
            (False, "Invalid file.")
        )

    def test_validate_file_invalid_file_type(self):
        """ Test validate file with invalid image file """

        invalid_image = Image.new("RGBA", (128, 128))

        invalid_image_buffer = BytesIO()
        invalid_image.save(invalid_image_buffer, format="ICO")

        bad_file = InMemoryUploadedFile(
            invalid_image_buffer,
            field_name=None,
            name="bad_file.txt",
            content_type="image/x-icon",
            size=invalid_image_buffer.tell(),
            charset=None,
        )

        self.assertEqual(
            validate_file(bad_file),
            (False, "Invalid file format.")
        )
