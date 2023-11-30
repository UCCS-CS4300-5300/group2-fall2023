### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Reservations Forms

""" Test Suite for the Reservations Form """

from django.test import TestCase
from Reservations import forms

class ReservationFormTests(TestCase):
    """ Test the ReservationForm form class """

    def test_valid_reservation_form(self):
        """ Test that the reservation form is recognized as valid """

        data = {
            "quantity": 12,
        }

        form = forms.ReservationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_reservation_form_missing_quantity(self):
        """ Test the reservation form when the quantity is missing """

        data = {}

        form = forms.ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_reservation_form_minimum_quantity(self):
        """ Test the reservation form when the quantity is below the minimum """

        data = {
            "quantity": 0
        }

        form = forms.ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
