### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Models

from django.test import TestCase
from decimal import Decimal
from Products.models import Product
from Events.models import Event

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


    def test_product_creation_with_market(self):
        """ Test valid product creation """

        name = "Product 1"
        description = "Product 1 Description"
        price = 3.45
        quantity = 10
        event = Event.objects.create(
            name="Event 1",
            location="Some Location",
            start_time="2025-04-12T00:00-00:00",
            end_time="2025-04-15T00:00-00:00",
        )

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            product_event=event,
        )

        self.assertTrue(Product.objects.filter(name=name).exists())
        
        product_1 = Product.objects.get(name=name)
        self.assertEqual(product_1.name, name)
        self.assertEqual(product_1.description, description)
        self.assertEqual(product_1.price, Decimal(str(price)))
        self.assertEqual(product_1.quantity, quantity)
        self.assertEqual(product_1.product_event.name, event.name)
        

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

    