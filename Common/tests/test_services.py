### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Models """

from io import BytesIO
from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from Products.models import Product
from Common.models import ProductImage
from Common.services import ImageService


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

        ImageService().create_image(
            self.valid_image_file,
            self.product,
            ProductImage,
        )

        self.assertTrue(self.product.image.count() == 1)
