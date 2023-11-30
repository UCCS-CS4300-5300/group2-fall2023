### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Reservations Models

""" Test Suite for the Reservations Model """

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from Products.models import Product
from Reservations.models import Reservation


class ReservationTests(TestCase):
    """ Test the Reservation model """

    def setUp(self):
        """ Set up the necessary testing data """

        self.product_owner = User.objects.create_user(
            username="product_owner",
            password="testingpassword"
        )
        self.product_owner.save()

        self.customer = User.objects.create_user(
            username="customer",
            password="testingpassword"
        )
        self.customer.save()

        self.product_price = 100.00
        self.product_quantity = 20

        self.product = Product.objects.create(
            name="test_product",
            description="Test description.",
            price=self.product_price,
            quantity=self.product_quantity,
            owner=self.product_owner,
        )
        self.product.save()


    def test_reservation_creation(self):
        """ Test successful reservation creation """

        quantity = 10

        Reservation.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=quantity,
            price=quantity*self.product_price,
        )

        self.assertTrue(Reservation.objects.filter(quantity=quantity).exists())

        reservation = Reservation.objects.get(quantity=quantity)
        self.assertEqual(reservation.product.pk, self.product.pk)
        self.assertEqual(reservation.customer.pk, self.customer.pk)
        self.assertEqual(reservation.quantity, quantity)
        self.assertEqual(reservation.price, quantity * self.product_price)


    def test_reservation_creation_max_quantity(self):
        """ Test successful reservation creation with maximum quantity """

        quantity = self.product_quantity

        Reservation.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=quantity,
            price=quantity*self.product_price,
        )

        self.assertTrue(Reservation.objects.filter(quantity=quantity).exists())


    def test_reservation_creation_minimum_quantity(self):
        """ Test failed reservation creation with quantity below minimum """

        quantity = 0

        with self.assertRaises(ValidationError) as context:
            reservation = Reservation.objects.create(
                product=self.product,
                customer=self.customer,
                quantity=quantity,
                price=quantity*self.product_price,
            )
            reservation.full_clean()

        self.assertIn("quantity", str(context.exception))
