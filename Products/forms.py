### CS 4300 Fall 2023 Group 2
### Harvestly
### Product Form

from django import forms
from Products.models import Product
from Events.models import Event
from Common.shared_models import Image


class ProductForm(forms.ModelForm):
    """Product upload form information"""

    # TODO need to add validators
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
            "product_event": forms.Select(),  # TODO this should be limited to only markets where the user is the organizer or has joined
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
            "price": "Product price",
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

    def clean_image(self):
        """Validate image size, ensure it is less than 5 MB"""
        image = self.cleaned_data.get("image")

        if image is None:
            return image

        max_file_size = 5242880  # file size: 5 MB
        min_file_size = 10240  # file size: 1 KB

        if image and image.size > max_file_size:
            raise forms.ValidationError("Image file too large. max size is 5 MB")
        elif image and image.size < min_file_size:
            raise forms.ValidationError("Image file too small. min size is 10 KB")

        return image


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

    def clean_reserve_quantity(self):
        """Clean quantity field, ensure it is at least 1"""

        reserve_quantity = self.cleaned_data.get("reserve_quantity")

        if reserve_quantity is None or reserve_quantity < 1:
            raise forms.ValidationError("Reserve quantity must be at least 1!")

        return reserve_quantity
