### CS 4300 Fall 2023 Group 2
### Harvestly
### Product Form

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """ Product upload form information """

    # TODO need to add validators
    # TODO need to add image upload
    # TODO need to link back to vendor

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "quantity",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"maxlength": 255, "placeholder": "Product name (max 255 characters)"}),
            "price": forms.NumberInput(attrs={"step": "0.01", "placeholder": "Product price"}),
            "quantity": forms.NumberInput(attrs={"step": "1", "min": "1", "placeholder": "Product quantity"}),
            "description": forms.Textarea(attrs={"rows": 5, "Placeholder": "Product description"}),
        }

        labels = {
            "name": "Product name",
            "price": "Product price",
            "quantity": "Product quantity",
            "description": "Product description",
        }