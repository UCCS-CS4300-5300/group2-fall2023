### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Views

from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Product
from .forms import ProductForm, ProductUpdateForm, ProductReserveForm


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
    """ Create View for an Event Object. URL `/products/new/` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm

    # Establish the target template for use
    template_name = "product_create.html"

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.object.pk})


class ProductDetails(DetailView):
    """ Product Details about a specific product. URL `/products/details/<int:pk>/` """

    # Set model type
    model = Product
    template_name = "product_detail.html"


class ProductUpdate(UpdateView):
    """ Edit product details of a specific product. URL `/products/edit/<int:pk>/` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductUpdateForm

    # Establish the target template for use
    template_name = "product_update.html"

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.object.pk})


class ProductDelete(DeleteView):
    """ Delete a specific product. URL `/products/delete/<int:pk>/` """

    # Establish the model type and template name for the generic view
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("products")
    

class ProductReserve(UpdateView):
    """ Reserve a quantity of a specific product. URL `/products/reserve/<int:pk>/` """

    # Establish the model type and form class for use
    model = Product
    form_class = ProductReserveForm

    # Establish the target template for use
    template_name = "product_reserve.html"

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.object.pk})

