### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Common Models

""" Test Suite for the Common Models """

from django.test import TestCase
from django.contrib.auth.models import User

from Common.models import ProductImage
from Products.models import Product


class ProductImageTests(TestCase):
    """ Tests for the ImageUpload model """

    def setUp(self):
        """ Set up for product image tests, create Product """

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

        self.product_image = ProductImage.objects.create(
            related_model = self.product,
        )

    def test_product_image_str_method(self):
        """ Test the `__str__` method """

        self.assertEqual(str(self.product_image), f"{self.product.name} image")

    def test_product_image_related_model_image_attribute(self):
        """ Test that the related model `image` attribute works """

        self.assertTrue(self.product.image.filter(pk=self.product_image.pk).exists())
