### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Views

from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product


class ProductList(ListView):
    """ Get a list of Harvestly products. URL `/get-products-list/` """

    def get(self, request):
        """ Query all products, render in product list template. """

        # Query products
        model = Product.objects.all()
        template_name = "product_list.html"
        
        # Pass products to events_list.html
        return render(request, template_name, {'product_list': model})
    
    
