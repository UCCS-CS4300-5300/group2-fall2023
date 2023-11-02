from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product

# Create your views here.


class ProductList(ListView):
    """Get a list of Harvestly products. URL `/get-products-list/`"""

    # Query products
    model = Product
    template_name = "products_list.html"
    context_object_name = "product_list"