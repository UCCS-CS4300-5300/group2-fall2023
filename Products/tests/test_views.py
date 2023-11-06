### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Views

from django.test import TestCase
from django.urls import reverse
from Products import models


class ProductListTests(TestCase):
    """ Test the product list view """

    def test_product_list_at_url(self):
        """ Verify that the product list exists at `/products/` """

        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)


    def test_product_list_at_reverse_lookup(self):
        """ Verify that the product list exists with reverse lookup of `products` """

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)


    def test_product_list_uses_template(self):
        """ Verify that the product list uses the correct template """

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("product_list.html")


    def test_product_list_uses_layout(self):
        """ Verify that the product list uses the layout template """

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("layout.html")


    def test_product_list_empty(self):
        """ Test the product list view, when no products exist """

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_list.html")
        self.assertTemplateUsed(response, "empty_list.html")


    def test_product_list_with_products(self):
        """ Test the product list view with product instances """

        product_1 = models.Product.objects.create(
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )

        product_2 = models.Product.objects.create(
            name="Product 2",
            description="Product 2 Description",
            price=12.00,
            quantity=11,
        )

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_list.html")
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)


class ProductCreateTests(TestCase):
    """ Test the product create view """

    def test_product_create_at_url(self):
        """ Verify that the product create exists at `/products/new` """

        response = self.client.get("/products/new")

        self.assertEqual(response.status_code, 200)


    def test_product_create_at_reverse_lookup(self):
        """ Verify that the product create exists with reverse lookup of `product-create` """

        response = self.client.get(reverse("product-create"))

        self.assertEqual(response.status_code, 200)


    def test_product_create_uses_template(self):
        """ Verify that the product create view uses the correct template """

        response = self.client.get(reverse("product-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_create.html")


    def test_product_create_uses_layout(self):
        """ Verify that the product create view uses the layout template """

        response = self.client.get(reverse("product-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")

    
    def test_product_creates_object(self):
        """ Verify that the product create view successfully creates a product """

        data = {
            "name": "Product 1",
            "description": "Product 1 Description",
            "price": 3.45,
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Product.objects.filter(name="Product 1").exists())


    def test_product_create_missing_name(self):
        """ Test the product create view post with missing name in data """

        data = {
            "description": "Product 1 Description",
            "price": 3.45,
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_missing_description(self):
        """ Test the product create view post with missing description in data """

        data = {
            "name": "Product 1",
            "price": 3.45,
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_missing_price(self):
        """ Test the product create view post with missing price in data """

        data = {
            "name": "Product 1",
            "description": "Description 1",
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_missing_quantity(self):
        """ Test the product create view post with missing quantity in data """

        data = {
            "name": "Product 1",
            "description": "Description 1",
            "price": 3.45,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_invalid_name_too_short(self):
        """ Test the product create view post with invalid name - too short """

        data = {
            "name": "",
            "description": "Product 1 Description",
            "price": 3.45,
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_invalid_name_too_long(self):
        """ Test the product create view post with invalid name - too long """

        data = {
            "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris blandit congue neque nec tristique. \
                Duis sed volutpat mi, et rutrum justo. Nunc condimentum feugiat erat in interdum. Proin eu mattis dolor. \
                Curabitur quis risus consectetur neque tempus ullamcorper. Aliquam venenatis purus at hendrerit vehicula. \
                Maecenas laoreet vitae elit in lacinia. Vestibulum tristique erat hendrerit dictum consequat. Sed at eleifend est. \
                Aenean et erat in ligula facilisis vestibulum nec non lectus.",
            "description": "Product 1 Description",
            "price": 3.45,
            "quantity": 10,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")


    def test_product_create_invalid_quantity_minimum(self):
        """ Test the product create view post with invalid name - too long """

        data = {
            "name": "Product 1",
            "description": "Product 1 Description",
            "price": 3.45,
            "quantity": 0,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors.")