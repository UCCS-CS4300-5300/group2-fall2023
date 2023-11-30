### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Reservations Views

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Products.models import Product
from Reservations.models import Reservation

class ReservationCreateTests(TestCase):
    """ Test the Reservation Create view """

    def setUp(self):
        """ Create a Product to reserve and login as a customer """

        product_owner_username = "product_owner"
        customer_username = "customer"
        password = "testingpassword"

        self.product_owner = User.objects.create_user(
            username=product_owner_username,
            password=password,
        )

        self.customer = User.objects.create_user(
            username=customer_username,
            password=password,
        )

        self.product_1 = Product.objects.create(
            id=1,
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
            owner=self.product_owner
        )

        self.client.login(username=customer_username, password=password)

    def test_reservation_create_at_url(self):
        """ Test that the reservation create view exists at `/reservations/new/<int:product_id>` """

        response = self.client.get(f"/reservations/new/{self.product_1.id}")

        self.assertEqual(response.status_code, 200)

    def test_reservation_create_at_reverse_lookup(self):
        """ Test that the reservation create view exists at reverse lookup of `reservation-create` """

        response = self.client.get(reverse("reservation-create", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)

    def test_reservation_create_uses_template(self):
        """ Test that the reservation create view uses correct template """

        response = self.client.get(reverse("reservation-create", args=[self.product_1.id]))

        self.assertTemplateUsed(response, "reservation_create.html")

    def test_reservation_create_uses_layout(self):
        """ Test that the reservation create view uses layout """

        response = self.client.get(reverse("reservation-create", args=[self.product_1.id]))

        self.assertTemplateUsed(response, "layout.html")

    def test_reservation_create_missing_object(self):
        """ Test reservation create view when `Product` object is missing """

        response = self.client.get(reverse("reservation-create", args=["999"]))

        self.assertEqual(response.status_code, 404)

    def test_reservation_create_valid(self):
        """ Test successful reservation creation"""

        quantity = 5
        data = {
            "quantity": quantity,
        }

        response = self.client.post(reverse("reservation-create", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reservation.objects.filter(quantity=quantity).exists())

        # check correct user and product
        reservation = Reservation.objects.get(quantity=quantity)
        self.assertEqual(reservation.product.id, self.product_1.id)
        self.assertEqual(reservation.customer.id, self.customer.id)

    def test_reservation_create_missing_quantity(self):
        """ Test the reservation create view with `quantity` missing """

        data = {}

        response = self.client.post(reverse("reservation-create", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All fields are required! Include a reservation quantity!")

    def test_reservation_create_quantity_maximum(self):
        """ Test the reservation create view with `quantity` greater than allowed """

        quantity = self.product_1.quantity + 1  # 1 more than allowed
        data = {
            "quantity": quantity,
        }

        response = self.client.post(reverse("reservation-create", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve quantity must not exceed product quantity!")

    def test_reservation_create_quantity_minimum(self):
        """ Test the reservation create view with `quantity` less than allowed """

        quantity = 0
        data = {
            "quantity": quantity,
        }

        response = self.client.post(reverse("reservation-create", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve quantity must be at least 1!")


class ReservationUpdateTests(TestCase):
    """ Test the Reservation Update view """


class ReservationDeleteTests(TestCase):
    """ Test the Reservation Delete view """