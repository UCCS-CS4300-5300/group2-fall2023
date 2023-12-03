### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Utilities Methods """

from io import BytesIO
from PIL import Image
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
            size=buffer.getbuffer().nbytes,
            charset=None,
        )

    def tearDown(self):
        """ Ensure that InMemoryUploadedFile objects are closed """

        self.valid_image_file.close()

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
        """ Test validate file with a non-image file """

        bad_file_content = b"Some file content"
        bad_file_buffer = BytesIO(bad_file_content)

        bad_file = InMemoryUploadedFile(
            bad_file_buffer,
            field_name=None,
            name="bad_file.txt",
            content_type="text/plain",
            size=bad_file_buffer.getbuffer().nbytes,
            charset=None,
        )

        self.assertEqual(
            validate_file(bad_file),
            (False, "Invalid file.")
        )

        bad_file.close()

    def test_validate_file_invalid_file_type(self):
        """ Test validate file with invalid image file """

        invalid_image = Image.new("RGBA", (128, 128))

        invalid_image_buffer = BytesIO()
        invalid_image.save(invalid_image_buffer, format="ICO")

        invalid_image_file = InMemoryUploadedFile(
            invalid_image_buffer,
            field_name=None,
            name="bad_file.txt",
            content_type="image/x-icon",
            size=invalid_image_buffer.getbuffer().nbytes,
            charset=None,
        )

        self.assertEqual(
            validate_file(invalid_image_file),
            (False, "Invalid file format.")
        )

        invalid_image_file.close()

    def test_validate_image_dimensions_bad_file(self):
        """ Test validate image dimensions with a non-image file """

        bad_file_content = b"Some file content"
        bad_file_buffer = BytesIO(bad_file_content)

        bad_file = InMemoryUploadedFile(
            bad_file_buffer,
            field_name=None,
            name="bad_file.txt",
            content_type="text/plain",
            size=bad_file_buffer.getbuffer().nbytes,
            charset=None,
        )

        self.assertEqual(
            validate_file(bad_file),
            (False, "Invalid file.")
        )

        bad_file.close()

    def test_validate_image_dimensions_invalid_dimensions(self):
        """ Test validate image dimensions with invalid image dimensions """

        invalid_image = Image.new("RGB", (
            ImageService.MAX_IMAGE_SIZE[0] + 1,
            ImageService.MAX_IMAGE_SIZE[0] + 1,
        ))

        invalid_image_buffer = BytesIO()
        invalid_image.save(invalid_image_buffer, format="JPEG")

        invalid_image_file = InMemoryUploadedFile(
            invalid_image_buffer,
            field_name=None,
            name="test_image.jpg",
            content_type="image/jpeg",
            size=invalid_image_buffer.getbuffer().nbytes,
            charset=None,
        )

        validation_result = validate_image_dimensions(invalid_image_file)
        self.assertEqual(validation_result[0], False)
        self.assertIn("exceeds maximum allowed", validation_result[1])

        invalid_image_file.close()

    def test_validate_file_size_minimum_file_size(self):
        """ Test validate file size with a file size below minimum """

        invalid_image_content = bytes([1 for _ in range(ImageService.MIN_FILE_SIZE - 1)])
        invalid_image_buffer = BytesIO(invalid_image_content)

        invalid_image_file = InMemoryUploadedFile(
            invalid_image_buffer,
            field_name=None,
            name="test_image.jpg",
            content_type="image/jpeg",
            size=invalid_image_buffer.getbuffer().nbytes,
            charset=None,
        )

        validation_result = validate_file_size(invalid_image_file)
        self.assertEqual(validation_result[0], False)
        self.assertIn("Image file too small.", validation_result[1])

        invalid_image_file.close()

    def test_validate_file_size_maximum_file_size(self):
        """ Test validate file size with a file size below maximum """

        invalid_image_content = bytes([1 for _ in range(ImageService.MAX_FILE_SIZE + 1)])
        invalid_image_buffer = BytesIO(invalid_image_content)

        invalid_image_file = InMemoryUploadedFile(
            invalid_image_buffer,
            field_name=None,
            name="test_image.jpg",
            content_type="image/jpeg",
            size=invalid_image_buffer.getbuffer().nbytes,
            charset=None,
        )

        validation_result = validate_file_size(invalid_image_file)
        self.assertEqual(validation_result[0], False)
        self.assertIn("Image file too large.", validation_result[1])

        invalid_image_file.close()
