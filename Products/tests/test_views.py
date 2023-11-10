### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Products Views

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Products.models import Product
from Products import views


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

        product_1 = Product.objects.create(
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )

        product_2 = Product.objects.create(
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

    def setUp(self):
        """ Login as user to handle LoginRequired """

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)


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
        self.assertTrue(Product.objects.filter(name="Product 1").exists())


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


class ProductDetailTests(TestCase):
    """ Test the Product Detail view """


    def setUp(self):
        """ Create an object to view details """
        
        self.product_1 = Product.objects.create(
            id=1,
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )

    
    def test_product_detail_at_url(self):
        """ Verify that the product detail exists at `/products/details/<int:pk>` """

        response = self.client.get(f"/products/details/{self.product_1.id}")

        self.assertEqual(response.status_code, 200)


    def test_product_detail_at_reverse_lookup(self):
        """ Verify that the product detail exists with reverse lookup of `product-details` """

        response = self.client.get(reverse("product-details", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_product_detail_uses_template(self):
        """ Verify that the product detail view uses the correct template """

        response = self.client.get(reverse("product-details", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_detail.html")


    def test_product_detail_uses_layout(self):
        """ Verify that the product detail view uses the layout template """

        response = self.client.get(reverse("product-details", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_product_detail_missing_object(self):
        """ Test the product detail view when there is no object at the given argument """

        response = self.client.get(reverse("product-details", args=["999"]))

        self.assertEqual(response.status_code, 404)


    def test_product_detail_displays_object_details(self):
        """ Test that the product detail view displays product details """

        response = self.client.get(reverse("product-details", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_1.description)
        self.assertContains(response, self.product_1.price)
        self.assertContains(response, self.product_1.quantity)


class ProductUpdateTests(TestCase):
    """ Test the Product Update view """

    def setUp(self):
        """ Login as user to handle LoginRequired and Create an object to be updated """

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

        self.product_1 = Product.objects.create(
            id=1,
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )

    def test_product_update_at_url(self):
        """ Verify that the product update exists at `/products/edit/<int:pk>` """

        response = self.client.get(f"/products/edit/{self.product_1.id}")

        self.assertEqual(response.status_code, 200)


    def test_product_update_at_reverse_lookup(self):
        """ Verify that the product update exists with reverse lookup of `product-update` """

        response = self.client.get(reverse("product-update", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_product_update_uses_template(self):
        """ Verify that the product update view uses the correct template """

        response = self.client.get(reverse("product-update", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_update.html")


    def test_product_update_uses_layout(self):
        """ Verify that the product update view uses the layout template """

        response = self.client.get(reverse("product-update", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_product_update_missing_object(self):
        """ Test the product update view when there is no object at the given argument """

        response = self.client.get(reverse("product-update", args=["999"]))

        self.assertEqual(response.status_code, 404)


    def test_product_update_displays_object_details(self):
        """ Test that the product update view displays product details (prior to being changed) """

        response = self.client.get(reverse("product-update", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_1.description)
        self.assertContains(response, self.product_1.price)
        self.assertContains(response, self.product_1.quantity)


    def test_product_update_change_name(self):
        """ Test that the product update view changes name successfully """

        new_name = "New Object Name"
        data = {
            "name": new_name,
            "description": self.product_1.description,
            "price": self.product_1.price,
            "quantity": self.product_1.quantity,
        }

        response = self.client.post(reverse("product-update", args=[self.product_1.id]), data)
        self.assertEqual(response.status_code, 302)

        # validate updated object
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.name, new_name)


    def test_product_update_change_description(self):
        """ Test that the product update view changes description successfully """

        new_description = "New Object Description"
        data = {
            "name": self.product_1.name,
            "description": new_description,
            "price": self.product_1.price,
            "quantity": self.product_1.quantity,
        }

        response = self.client.post(reverse("product-update", args=[self.product_1.id]), data)
        self.assertEqual(response.status_code, 302)

        # validate updated object
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.description, new_description)


    def test_product_update_change_price(self):
        """ Test that the product update view changes price successfully """

        new_price = 100.00
        data = {
            "name": self.product_1.name,
            "description": self.product_1.description,
            "price": new_price,
            "quantity": self.product_1.quantity,
        }

        response = self.client.post(reverse("product-update", args=[self.product_1.id]), data)
        self.assertEqual(response.status_code, 302)

        # validate updated object
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.price, new_price)


    def test_product_update_change_quantity(self):
        """ Test that the product update view changes quantity successfully """

        new_quantity = 20
        data = {
            "name": self.product_1.name,
            "description": self.product_1.description,
            "price": self.product_1.price,
            "quantity": new_quantity,
        }

        response = self.client.post(reverse("product-update", args=[self.product_1.id]), data)
        self.assertEqual(response.status_code, 302)

        # validate updated object
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.quantity, new_quantity)


class ProductDeleteTests(TestCase):
    """ Test the Product Delete view """

    def setUp(self):
        """ Login as user to handle LoginRequired and Create an object to be deleted """

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

        self.product_1 = Product.objects.create(
            id=1,
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )


    def test_product_delete_at_url(self):
        """ Verify that the product delete exists at `/products/delete/<int:pk>` """

        response = self.client.get(f"/products/delete/{self.product_1.id}")

        self.assertEqual(response.status_code, 200)


    def test_product_delete_at_reverse_lookup(self):
        """ Verify that the product delete exists with reverse lookup of `product-delete` """

        response = self.client.get(reverse("product-delete", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_product_delete_uses_template(self):
        """ Verify that the product delete view uses the correct template """

        response = self.client.get(reverse("product-delete", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_delete.html")


    def test_product_delete_uses_layout(self):
        """ Verify that the product delete view uses the layout template """

        response = self.client.get(reverse("product-delete", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_product_delete_missing_object(self):
        """ Test the product delete view when there is no object at the given argument """

        response = self.client.get(reverse("product-delete", args=["999"]))

        self.assertEqual(response.status_code, 404)

    
    def test_product_delete_valid(self):
        """ Test the product delete post with a valid object ID """

        response = self.client.post(reverse("product-delete", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product_1.id).exists())


class ProductReserveTests(TestCase):
    """ Test the Product Reserve view """

    def setUp(self):
        """ Login as user to handle LoginRequired and Create an object to be reserved """

        username = "test_user"
        password = "test_password"

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        user.save()
        self.client.login(username=username, password=password)

        self.product_1 = Product.objects.create(
            id=1,
            name="Product 1",
            description="Product 1 Description",
            price=3.45,
            quantity=10,
        )


    def test_product_reserve_at_url(self):
        """ Verify that the product reserve exists at `/products/reserve/<int:pk>` """

        response = self.client.get(f"/products/reserve/{self.product_1.id}")

        self.assertEqual(response.status_code, 200)


    def test_product_reserve_at_reverse_lookup(self):
        """ Verify that the product reserve exists with reverse lookup of `product-reserve` """

        response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)


    def test_product_reserve_uses_template(self):
        """ Verify that the product reserve view uses the correct template """

        response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_reserve.html")


    def test_product_reserve_uses_layout(self):
        """ Verify that the product reserve view uses the layout template """

        response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout.html")


    def test_product_reserve_missing_object(self):
        """ Test the product reserve view when there is no object at the given argument """

        response = self.client.get(reverse("product-reserve", args=["999"]))

        self.assertEqual(response.status_code, 404)


    def test_product_reserve_valid(self):
        """ Test the product reserve view with successful reservation """

        original_quantity = self.product_1.quantity
        reserve_quantity = 5
        data = {
            "reserve_quantity": reserve_quantity,
        }

        response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 302)

        # validate updated object
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.quantity, original_quantity - reserve_quantity)


    def test_product_reserve_quantity_maximum(self):
        """ Test the product reserve view with `reserve_quantity` greater than allowed """

        original_quantity = self.product_1.quantity
        reserve_quantity = self.product_1.quantity + 1
        data = {
            "reserve_quantity": reserve_quantity,
        }

        response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve quantity must not exceed available quantity!")

        # validate that the object is not updated
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.quantity, original_quantity)


    def test_product_reserve_quantity_minimum(self):
        """ Test the product reserve view with `reserve_quantity` less than allowed """

        original_quantity = self.product_1.quantity
        reserve_quantity = 0
        data = {
            "reserve_quantity": reserve_quantity,
        }

        response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve quantity must be at least 1!")

        # validate that the object is not updated
        updated = Product.objects.get(id=self.product_1.id)
        self.assertEqual(updated.quantity, original_quantity)