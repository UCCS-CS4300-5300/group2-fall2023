### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Models

from django.test import TestCase
from decimal import Decimal
from Products.models import Product

# TODO - update this when image imports are available

class ProductTests(TestCase):
    """ Test the Product model """

    def test_product_creation(self):
        """ Test valid product creation """

        name = "Product 1"
        description = "Product 1 Description"
        price = 3.45
        quantity = 10

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )

        self.assertTrue(Product.objects.filter(name=name).exists())
        
        product_1 = Product.objects.get(name=name)
        self.assertEqual(product_1.name, name)
        self.assertEqual(product_1.description, description)
        self.assertEqual(product_1.price, Decimal(str(price)))
        self.assertEqual(product_1.quantity, quantity)


    def test_product_str(self):
        """ Test the product `__str__` method """

        name = "Product 1"

        product_1 = Product.objects.create(
            name=name,
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )

        self.assertEqual(product_1.name, name)

    