### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Models """

from unittest.mock import MagicMock
from io import BytesIO
from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from Products.models import Product
from Common.models import ProductImage
from Common.services import ImageService
from Common.forms import ProductImageForm


class ImageServiceTests(TestCase):
    """ Test for the ImageService service """

    def setUp(self):
        """ Set up for ImageServiceTests """

        valid_image = Image.new("RGB", (
            ImageService.DEFAULT_IMAGE_WIDTH,
            ImageService.DEFAULT_IMAGE_HEIGHT,
        ))

        buffer = BytesIO()
        valid_image.save(buffer, format="JPEG")
        buffer.seek(0)

        self.valid_image_file = SimpleUploadedFile(
            "test_image.jpg",
            buffer.read(),
            content_type="image/jpeg",
        )

        self.product_owner = User.objects.create_user(
            username="testingusername",
            password="testingpassword",
        )
        self.product_owner.save()

        self.product = Product.objects.create(
            name="test_product",
            description="Test description.",
            price=10.00,
            quantity=5,
            owner=self.product_owner,
        )
        self.product.save()

    def test_create_image(self):
        """ Test successful create image call """

        image_instance = ImageService().create_image(
            self.valid_image_file,
            self.product,
            ProductImage,
        )

        self.assertEqual(self.product.image.count(), 1)
        # verify image exists
        self.assertTrue(image_instance.file)

    def test_handle_image_update_with_new_image(self):
        """ Test handle image update with a new image """

        # create mock image form with new file data
        image_form = MagicMock(spec=ProductImageForm)
        image_form.cleaned_data = {
            "file": self.valid_image_file,
            "alt_text": "test alt text",
        }
        image_form.changed_data = ["file"]

        # call handle_image_update
        ImageService().handle_image_update(image_form, self.product, ProductImage)

        # Assert new image instance is created
        self.assertEqual(self.product.image.count(), 1)

    def test_image_update_with_existing_image(self):
        """ Test image update with existing image """

        # create existing image instance
        existing_image = ImageService().create_image(
            self.valid_image_file,
            self.product,
            ProductImage,
        )

        # create mock image form with new file data
        image_form = MagicMock(spec=ProductImageForm)
        image_form.cleaned_data = {
            "file": self.valid_image_file,
            "alt_text": "test alt text",
        }
        image_form.changed_data = ["file"]

        # call handle_image_update
        ImageService().handle_image_update(image_form, self.product, ProductImage)

        # assert existing image is replaced
        self.assertEqual(self.product.image.count(), 1)
        self.assertNotEqual(self.product.image.first(), existing_image)

    def test_handle_image_update_with_no_file_change(self):
        """ Test image update with no file """

        image_form = MagicMock(spec=ProductImageForm)
        image_form.changed_data = []

        # call handle_image_update
        ImageService().handle_image_update(image_form, self.product, ProductImage)

        # Assert no new image instance is created
        self.assertTrue(self.product.image.count() == 0)

    def test_handle_image_update_clear(self):
        """ Test image update with clear """

        image_form = MagicMock(spec=ProductImageForm)
        image_form.cleaned_data = {
            "file": None,
            "alt_text": "test alt text",
        }
        image_form.changed_data = ["file"]

        existing_image = ImageService().create_image(
            self.valid_image_file,
            self.product,
            ProductImage,
        )

        # call handle_image_update
        ImageService().handle_image_update(image_form, self.product, ProductImage)

        # Assert no new image instance is created
        self.assertTrue(self.product.image.count() == 0)
        # Assert existing image is deleted
        self.assertFalse(existing_image.file.storage.exists(existing_image.file.name))

    def test_create_thumbnail(self):
        """ Test create thumbnail """

        thumb_path = "thumbnails/thumb_test_image.jpg"
        thumbnail = ImageService().create_thumbnail(self.valid_image_file, thumb_path)

        # check thumbnail is created
        self.assertIsNotNone(thumbnail)

    def test_resize_image(self):
        """ Test resize image """

        # Call resize_image
        resized_image = ImageService().resize_image(self.valid_image_file)

        # Check if the image is resized
        self.assertIsNotNone(resized_image)

    def test_generate_unique_filename(self):
        """ Test generate unique filename """

        image_service = ImageService()

        # Create filename
        filename = "test_image.jpg"

        # Call generate_unique_filename
        unique_filename = image_service.generate_unique_filename(filename)

        # Check if the unique filename is generated
        self.assertIsNotNone(unique_filename)

    def test_file_names_are_unique(self):
        """test that file names are unique"""

        # create filename
        filename = "test_image.jpg"

        # call generate_unique_filename
        unique_filename = ImageService().generate_unique_filename(filename)
        unique_filename_2 = ImageService().generate_unique_filename(filename)

        # check names are unique
        self.assertNotEqual(unique_filename, unique_filename_2)
