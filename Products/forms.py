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

    def clean_quantity(self):
        """ Clean quantity field, ensure it is at least 1 """
        
        quantity = self.cleaned_data.get("quantity")
        
        if quantity is not None and quantity < 1:
            raise forms.ValidationError("Value must be greater than or equal to 1")
        
        return quantity


class ProductReserveForm(forms.Form):
    """ Product reserve form, for user to reserve a quantity of a product """

    reserve_quantity = forms.IntegerField()

    class Meta:
        labels = {
            "reserve_quantity": "Reserve Quantity",
        }

        widgets = {
            "reserve_quantity": forms.NumberInput(attrs={"step": "1", "min": "1", "placeholder": "Reserve quantity"}),
        }


    def clean_reserve_quantity(self):
        """ Clean quantity field, ensure it is at least 1 """
        
        reserve_quantity = self.cleaned_data.get("reserve_quantity")
        
        if reserve_quantity is not None and reserve_quantity < 1:
            raise forms.ValidationError("Value must be greater than or equal to 1")
        
        return reserve_quantity