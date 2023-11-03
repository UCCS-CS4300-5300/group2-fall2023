### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Views

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Product
from .forms import ProductForm


class ProductList(ListView):
    """ Get a list of Harvestly products. URL `/get-products-list/` """

    def get(self, request):
        """ Query all products, render in product list template. """

        # Query products
        model = Product.objects.all()
        template_name = "product_list.html"
        
        # Pass products to events_list.html
        return render(request, template_name, {'product_list': model})
    

class ProductCreate(CreateView):
    """ Create View for an Event Object. URL `/events/new` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm

    # Establish the target template for use
    template_name = "product_create.html"