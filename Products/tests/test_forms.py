### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Forms

from django.test import TestCase
from Products.forms import ProductForm, ProductReserveForm


class ProductFormTest(TestCase):
    """ Test the ProductForm form class """

    def test_valid_product_form(self):
        """ Test the product form is recognized as valid """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
        }

        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())


    def test_product_form_name_too_long(self):
        """ Test the product form when the provided name is too long """

        data = {
            "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris blandit congue neque nec tristique. \
                Duis sed volutpat mi, et rutrum justo. Nunc condimentum feugiat erat in interdum. Proin eu mattis dolor. \
                Curabitur quis risus consectetur neque tempus ullamcorper. Aliquam venenatis purus at hendrerit vehicula. \
                Maecenas laoreet vitae elit in lacinia. Vestibulum tristique erat hendrerit dictum consequat. Sed at eleifend est. \
                Aenean et erat in ligula facilisis vestibulum nec non lectus.",
            "price": 2.12,
            "quantity": 17,
            "description": "Some Product Description",
        }

        form = ProductForm(data=data)
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

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)


    def test_product_form_missing_name(self):
        """ Test form when name is missing """

        data = {
            "price": 2.12,
            "quantity": 12,
            "description": "Some Product Description",
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


    def test_product_form_missing_price(self):
        """ Test form when price is missing """

        data = {
            "name": "Some Product",
            "quantity": 12,
            "description": "Some Product Description",
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)


    def test_product_form_missing_quantity(self):
        """ Test form when quantity is missing """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "description": "Some Product Description",
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)


    def test_product_form_missing_description(self):
        """ Test form when description is missing """

        data = {
            "name": "Some Product",
            "price": 2.12,
            "quantity": 3,
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)


class ProductReserveFormTests(TestCase):
    """ Test the ProductReserveForm form class """

    def test_valid_product_reserve_form(self):
        """ Test the product reserve form is recognized as valid """

        data = {
            "reserve_quantity": 1,
        }

        form = ProductReserveForm(data=data)
        self.assertTrue(form.is_valid())

    
    def test_product_reserve_form_minimum_reserve_quantity(self):
        """ Test the product reserve form when the reserve quantity is less than the minimum """

        data = {
            "reserve_quantity": 0,
        }

        form = ProductReserveForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("reserve_quantity", form.errors)


    def test_product_reserve_form_missing_reserve_quantity(self):
        """ Test form when reserve quantity is missing """

        data = {}

        form = ProductReserveForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("reserve_quantity", form.errors)