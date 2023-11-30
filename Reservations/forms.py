### CS 4300 Fall 2023 Group 2
### Harvestly
### Reservation Form

""" Implementation of Reservation Model Form """

from django import forms
from Reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    """ Product reserve form, for user to reserve a quantity of a product """

    class Meta:
        """ Meta class for Reservation form """

        model = Reservation
        fields = [
            "quantity",
        ]

        labels = {
            "quantity": "Reservation Quantity",
        }

        widgets = {
            "quantity": forms.NumberInput(attrs={
                "step": "1",
                "min": "1",
                "placeholder": "1"
            }),
        }

        error_messages = {
            "quantity": {
                "required": "All fields are required! Include a reservation quantity!",
                "min_value": "Reserve quantity must be at least 1!",
            },
        }
