### CS 4300 Fall 2023 Group 2
### Harvestly
### Product Form

from django import forms
from Products.models import Product
from Events.models import Event


class ProductForm(forms.ModelForm):
    """Product upload form information"""

    # TODO need to add image upload

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "quantity",
            "product_event",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "required": "required",
                    "maxlength": "255",
                    "placeholder": "Product name (max 255 characters)",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "required": "required",
                    "min": "0.01",
                    "max": "100000.00",
                    "step": "0.01",
                    "placeholder": "X.XX",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "required": "required",
                    "step": "1",
                    "min": "1",
                    "placeholder": "Product quantity",
                }
            ),
            "product_event": forms.Select(),
            "description": forms.Textarea(
                attrs={
                    "required": "required",
                    "rows": 5,
                    "Placeholder": "Product description",
                }
            ),
        }

        labels = {
            "name": "Product name",
            "price": "Product price (USD)",
            "quantity": "Product quantity",
            "product_event": "Market for Product (optional)",
            "description": "Product description",
        }

    def clean_quantity(self):
        """Clean quantity field, ensure it is at least 1"""

        quantity = self.cleaned_data.get("quantity")

        if quantity is None or quantity < 1:
            raise forms.ValidationError("Value must be greater than or equal to 1")

        return quantity


class ProductReserveForm(forms.Form):
    """Product reserve form, for user to reserve a quantity of a product"""

    reserve_quantity = forms.IntegerField()

    class Meta:
        labels = {
            "reserve_quantity": "Reserve Quantity",
        }

        widgets = {
            "reserve_quantity": forms.NumberInput(
                attrs={
                    "required": "required",
                    "step": "1",
                    "min": "1",
                    "placeholder": "Reserve quantity",
                }
            ),
        }

        error_messages = {
            "reserve_quantity": {
                "required": "All fields are required! Include a reserve quantity!"
            },
        }

    def clean_reserve_quantity(self):
        """Clean quantity field, ensure it is at least 1"""

        reserve_quantity = self.cleaned_data.get("reserve_quantity")

        if reserve_quantity is None or reserve_quantity < 1:
            raise forms.ValidationError("Reserve quantity must be at least 1!")

        return reserve_quantity
