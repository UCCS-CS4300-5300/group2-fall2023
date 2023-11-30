### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Forms

""" Test Suite for the Product Form """

from django.test import TestCase
from django.contrib.auth.models import User

from Products import forms
from Events.models import Event


class ProductFormTest(TestCase):
    """ Test the ProductForm form class """

    def test_valid_product_form_without_market(self):
        """ Test the product form is recognized as valid """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertTrue(form.is_valid())


    def test_valid_product_form_with_market(self):
        """ Test the product form is recognized as valid """

        user = User.objects.create_user(username="testinguser", password="testingpassword")
        user.save()

        event = Event.objects.create(
            name="Market 1",
            location="Some Location",
            start_time="2025-04-12T00:00-00:00",
            end_time="2025-04-15T00:00-00:00",
            organizer=user
        )

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
            "product_event": event.pk,
        }

        form = forms.ProductForm(data=data)
        self.assertTrue(form.is_valid())


    def test_product_form_name_too_long(self):
        """ Test the product form when the provided name is too long """

        data = {
            "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris blandit \
                congue neque nec tristique. Duis sed volutpat mi, et rutrum justo. Nunc \
                condimentum feugiat erat in interdum. Proin eu mattis dolor. Curabitur quis \
                risus consectetur neque tempus ullamcorper. Aliquam venenatis purus at \
                hendrerit vehicula. Maecenas laoreet vitae elit in lacinia. Vestibulum tristique \
                erat hendrerit dictum consequat. Sed at eleifend est. Aenean et erat in ligula \
                facilisis vestibulum nec non lectus.",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


    def test_product_form_minimum_quantity(self):
        """ Test the product form when the quantity is less than the minimum """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 0,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)


    def test_product_form_missing_name(self):
        """ Test form when name is missing """

        data = {
            "price": 2.12,
            "quantity": 12,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


    def test_product_form_missing_price(self):
        """ Test form when price is missing """

        data = {
            "name": "Some Product",
            "quantity": 12,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)


    def test_product_form_missing_quantity(self):
        """ Test form when quantity is missing """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "description": "Some Product Description",
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)


    def test_product_form_missing_description(self):
        """ Test form when description is missing """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 3,
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)


    def test_product_form_invalid_event(self):
        """ Test product form when event is invalid """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
            "product_event": 999,
        }

        form = forms.ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("product_event", form.errors)
