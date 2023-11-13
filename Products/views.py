### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Views

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from .forms import ProductForm, ProductReserveForm


class ProductList(ListView):
    """ Get a list of Harvestly products. URL `/get-products-list/` """

    # Specify model and template
    model = Product
    template_name = "product_list.html"
    context_object_name = "product_list"
    

class ProductCreate(LoginRequiredMixin, CreateView):
    """ Create View for an Event Object. URL `/products/new/` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm

    # Establish the target template for use
    template_name = "product_create.html"

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.object.pk})


class ProductDetail(DetailView):
    """ Product Details about a specific product. URL `/products/details/<int:pk>/` """

    # Set model type
    model = Product
    template_name = "product_detail.html"


class ProductUpdate(LoginRequiredMixin, UpdateView):
    """ Edit product details of a specific product. URL `/products/edit/<int:pk>/` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm

    # Establish the target template for use
    template_name = "product_update.html"

    def get_success_url(self):
        """ Get success URL after post completion. """
        return reverse("product-details", kwargs={"pk": self.object.pk})


class ProductDelete(LoginRequiredMixin, DeleteView):
    """ Delete a specific product. URL `/products/delete/<int:pk>/` """

    # Establish the model type and template name for the generic view
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        """ Get success URL after post completion """

        return reverse("products")
    

class ProductReserve(LoginRequiredMixin, View):
    """ Reserve a quantity of a specific product. URL `/products/reserve/<int:pk>/` """

    template_name = "product_reserve.html"

    def get(self, request, pk):
        """ Handle get request to view (render form) """
        
        product = get_object_or_404(Product, pk=pk)
        form = ProductReserveForm

        return render(request, self.template_name, {"form": form, "product": product})


    def post(self, request, pk):
        """ Handle post request """

        product = get_object_or_404(Product, pk=pk)
        form = ProductReserveForm(request.POST)

        if form.is_valid():
            reserve_quantity = form.cleaned_data["reserve_quantity"]

            if reserve_quantity <= product.quantity:
                product.quantity -= reserve_quantity
                product.save()
                return HttpResponseRedirect(self.get_success_url(pk))

            form.add_error("reserve_quantity", "Reserve quantity must not exceed available quantity!")

        return render(request, self.template_name, {"form": form, "product": product})


    def get_success_url(self, pk):
        """ Get success URL after post completion """
        
        return reverse("product-details", kwargs={"pk": pk})
