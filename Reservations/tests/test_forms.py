
""" TODO """
# class ProductReserveFormTests(TestCase):
#     """ Test the ProductReserveForm form class """

#     def test_valid_product_reserve_form(self):
#         """ Test the product reserve form is recognized as valid """

#         data = {
#             "reserve_quantity": 1,
#         }

#         form = forms.ProductReserveForm(data=data)
#         self.assertTrue(form.is_valid())

    
#     def test_product_reserve_form_minimum_reserve_quantity(self):
#         """ Test the product reserve form when the reserve quantity is less than the minimum """

#         data = {
#             "reserve_quantity": 0,
#         }

#         form = forms.ProductReserveForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn("reserve_quantity", form.errors)


#     def test_product_reserve_form_missing_reserve_quantity(self):
#         """ Test form when reserve quantity is missing """

#         data = {}

#         form = forms.ProductReserveForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn("reserve_quantity", form.errors)