
""" TODO """

# class ProductReserveTests(TestCase):
#     """ Test the Product Reserve view """

#     def setUp(self):
#         """ Login as user to handle LoginRequired and Create an object to be reserved """

#         username = "test_user"
#         password = "test_password"

#         self.user = User.objects.create_user(
#             username=username,
#             password=password,
#         )

#         self.user.save()
#         self.client.login(username=username, password=password)

#         self.product_1 = Product.objects.create(
#             name="Product 1",
#             description="Product 1 Description",
#             price=3.45,
#             quantity=10,
#             owner=self.user
#         )

#     def test_product_reserve_at_url(self):
#         """ Verify that the product reserve exists at `/products/reserve/<int:pk>` """

#         response = self.client.get(f"/products/reserve/{self.product_1.id}")

#         self.assertEqual(response.status_code, 200)


#     def test_product_reserve_at_reverse_lookup(self):
#         """ Verify that the product reserve exists with reverse lookup of `product-reserve` """

#         response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

#         self.assertEqual(response.status_code, 200)


#     def test_product_reserve_uses_template(self):
#         """ Verify that the product reserve view uses the correct template """

#         response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

#         self.assertTemplateUsed(response, "product_reserve.html")


#     def test_product_reserve_uses_layout(self):
#         """ Verify that the product reserve view uses the layout template """

#         response = self.client.get(reverse("product-reserve", args=[self.product_1.id]))

#         self.assertTemplateUsed(response, "layout.html")


#     def test_product_reserve_missing_object(self):
#         """ Test the product reserve view when there is no object at the given argument """

#         response = self.client.get(reverse("product-reserve", args=["999"]))

#         self.assertEqual(response.status_code, 404)


#     def test_product_reserve_valid(self):
#         """ Test the product reserve view with successful reservation """

#         original_quantity = self.product_1.quantity
#         reserve_quantity = 5
#         data = {
#             "reserve_quantity": reserve_quantity,
#         }

#         response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

#         self.assertEqual(response.status_code, 302)

#         # validate updated object
#         updated = Product.objects.get(id=self.product_1.id)
#         self.assertEqual(updated.quantity, original_quantity - reserve_quantity)


#     def test_product_reserve_quantity_maximum(self):
#         """ Test the product reserve view with `reserve_quantity` greater than allowed """

#         original_quantity = self.product_1.quantity
#         reserve_quantity = self.product_1.quantity + 1
#         data = {
#             "reserve_quantity": reserve_quantity,
#         }

#         response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Reserve quantity must not exceed available quantity!")

#         # validate that the object is not updated
#         updated = Product.objects.get(id=self.product_1.id)
#         self.assertEqual(updated.quantity, original_quantity)


#     def test_product_reserve_quantity_minimum(self):
#         """ Test the product reserve view with `reserve_quantity` less than allowed """

#         original_quantity = self.product_1.quantity
#         reserve_quantity = 0
#         data = {
#             "reserve_quantity": reserve_quantity,
#         }

#         response = self.client.post(reverse("product-reserve", args=[self.product_1.id]), data)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Reserve quantity must be at least 1!")

#         # validate that the object is not updated
#         updated = Product.objects.get(id=self.product_1.id)
#         self.assertEqual(updated.quantity, original_quantity)