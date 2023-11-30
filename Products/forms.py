### CS 4300 Fall 2023 Group 2
### Harvestly
### Product Form

""" Implementation of Product Form """

from django import forms
from Products.models import Product


class ProductForm(forms.ModelForm):
    """ Product upload form information """

    class Meta:
        """ Meta class for Product Form """

        model = Product
        fields = [
            "name",
            "price",
            "quantity",
            "product_event",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "required": "required",
                "maxlength": "255", 
                "placeholder": "Product name (max 255 characters)"
            }),
            "price": forms.NumberInput(attrs={
                "required": "required",
                "min": "0.01",
                "max": "100000.00",
                "step": "0.01",
                "placeholder": "X.XX"
            }),
            "quantity": forms.NumberInput(attrs={
                "required": "required",
                "step": "1",
                "min": "1",
                "placeholder": "Product quantity"
            }),
            "product_event": forms.Select(),
            "description": forms.Textarea(attrs={
                "required": "required",
                "rows": 5,
                "Placeholder": "Product description"
            }),
        }

        labels = {
            "name": "Product name",
            "price": "Product price (USD)",
            "quantity": "Product quantity",
            "product_event": "Market for Product (optional)",
            "description": "Product description",
        }

        error_messages = {
            "name": {
                "required": "All fields are required! Include a name!",
                "max_length": "Maximum name length exceeded! Name length must not exceed \
                    255 characters!"
            },
            "price": {
                "required": "All fields are required! Include a price!",
                "min_value": "Price must be at least $0.01!",
                "max_value": "Price must not exceed $100,000.00!",
            },
            "quantity": {
                "required": "All fields are required! Include a quantity!",
                "max_value": "Maximum quantity exceeded! Maximum quantity \
                    for any one item is 100,000!",
            },
            "description": {
                "required": "All fields are required! Include a description!"
            },
        }


    def clean_quantity(self):
        """ Clean quantity field, ensure it is at least 1 
        
        Note that the minimum value on the model is 0, however, in the form entry
        the user must enter a value of at least 1.
        """

        quantity = self.cleaned_data.get("quantity")

        if quantity < 1:
            raise forms.ValidationError(
                "Minimum quantity requirement not met! Minimum quantity for an item is 1!"
            )

        return quantity
