### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Models

""" Test Suite for the Product Model """

from django.test import TestCase
from django.contrib.auth.models import User

from Products.models import Product
from Events.models import Event
from Reservations.models import Reservation


class ProductTests(TestCase):
    """ Test the Product model """

    def setUp(self):
        """Set up the necessary testing data"""

        self.user = User.objects.create_user(username="testinguser", password="testingpassword")
        self.user.save()

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
            owner=self.user
        )

        self.assertTrue(Product.objects.filter(name=name).exists())

        product_1 = Product.objects.get(name=name)
        self.assertEqual(product_1.name, name)
        self.assertEqual(product_1.description, description)
        self.assertEqual(product_1.price, price)
        self.assertEqual(product_1.quantity, quantity)

    def test_product_creation_with_market(self):
        """ Test valid product creation with the addition of an Event object """

        name = "Product 1"
        description = "Product 1 Description"
        price = 3.45
        quantity = 10
        event = Event.objects.create(
            name="Event 1",
            location="Some Location",
            start_time="2025-04-12T00:00-00:00",
            end_time="2025-04-15T00:00-00:00",
            organizer=self.user
        )

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            product_event=event,
            owner=self.user
        )

        self.assertTrue(Product.objects.filter(name=name).exists())

        product_1 = Product.objects.get(name=name)
        self.assertEqual(product_1.name, name)
        self.assertEqual(product_1.description, description)
        self.assertEqual(product_1.price, price)
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
            owner=self.user
        )

        self.assertEqual(product_1.name, name)

    def test_product_get_reservation_count(self):
        """ Test the product `get_reservation_count` method """

        product = Product.objects.create(
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
            owner=self.user
        )

        customer = User.objects.create_user(username="customer", password="testingpassword")
        customer.save()

        reserve_quantity = 5

        Reservation.objects.create(
            product=product,
            customer=customer,
            quantity=reserve_quantity,
            price=reserve_quantity*product.price,
        )

        self.assertEqual(product.get_reservation_count(), reserve_quantity)
