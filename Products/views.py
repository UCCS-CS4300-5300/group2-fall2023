### CS 4300 Fall 2023 Group 2
### Harvestly
### Products Views

from typing import Any
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from .forms import ProductForm, ProductReserveForm
from Common.forms import ImageUploadForm
from Events.models import Event
from Common.models import ProductImage
from Common.mixins import ImageHandlingMixin


class ProductList(ListView):
    """Get a list of Harvestly products. URL `/get-products-list/`"""

    # Specify model and template
    model = Product
    template_name = "product_list.html"
    context_object_name = "product_list"


# TODO create new create view, inherit from `View` class


class ProductCreate(LoginRequiredMixin, ImageHandlingMixin, CreateView):
    """Create View for an Event Object. URL `/products/new/`"""

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm
    image_form_class = ImageUploadForm

    # Establish the target template for use
    template_name = "product_create.html"

    def form_valid(self, form):
        """Update the `owner` field after submission"""
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()

        image_form = self.image_form_class(self.request.POST, self.request.FILES)

        self.handle_image_form(product, image_form)

        return super().form_valid(form)

    def get_success_url(self):
        """Get success URL after post completion."""

        return reverse("product-details", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Include list of events in context data"""

        # In order to iterate over the model options, we need to provide the list in
        #   the context. Unfortunately, iterating through Choice Select options is not
        #   supported in this version of Django.

        context = super().get_context_data(**kwargs)
        context[
            "event_list"
        ] = (
            Event.objects.all()
        )  # TODO update to be only the objects the user has access to

        return context

    def handle_image_form(self, model_instance, image_form):
        if 'file' in image_form.cleaned_data:
            image_upload = image_form.save()
            ProductImage.objects.create(product=model_instance, image=image_upload)

class ProductDetail(DetailView):
    """Product Details about a specific product. URL `/products/details/<int:pk>/`"""

    # Set model type
    model = Product
    template_name = "product_detail.html"


class ProductUpdate(LoginRequiredMixin, ImageHandlingMixin, UpdateView):
    """Edit product details of a specific product. URL `/products/edit/<int:pk>/`"""

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm
    image_form_class = ImageUploadForm

    # Establish the target template for use
    template_name = "product_update.html"

    def form_valid(self, form):
        product = form.save()

        image_form = self.image_form_class(
            self.request.POST, self.request.FILES, instance=self.get_image_instance()
        )

        self.handle_image_form(product, image_form)

        return super().form_valid(form)

    def get_success_url(self):
        """Get success URL after post completion."""

        return reverse("product-details", kwargs={"pk": self.object.pk})

    def handle_image_form(self, model_instance, image_form):
        if image_form.is_valid(): 
            file = image_form.cleaned_data.get("file")
            if file:
                image_upload = image_form.save()
                ProductImage.objects.update_or_create(product=model_instance, image=image_upload)
            elif file is None and not image_form.instance.file:
                ProductImage.objects.filter(product=model_instance).delete()

class ProductDelete(LoginRequiredMixin, DeleteView):
    """Delete a specific product. URL `/products/delete/<int:pk>/`"""

    # Establish the model type and template name for the generic view
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        """Get success URL after post completion"""

        return reverse("products")


class ProductReserve(LoginRequiredMixin, View):
    """Reserve a quantity of a specific product. URL `/products/reserve/<int:pk>/`"""

    template_name = "product_reserve.html"

    def get(self, request, pk):
        """Handle get request to view (render form)"""

        product = get_object_or_404(Product, pk=pk)
        form = ProductReserveForm

        return render(request, self.template_name, {"form": form, "product": product})

    def post(self, request, pk):
        """Handle post request"""

        product = get_object_or_404(Product, pk=pk)
        form = ProductReserveForm(request.POST)

        if form.is_valid():
            reserve_quantity = form.cleaned_data["reserve_quantity"]

            if reserve_quantity <= product.quantity:
                product.quantity -= reserve_quantity
                product.save()
                return HttpResponseRedirect(self.get_success_url(pk))

            form.add_error(
                "reserve_quantity",
                "Reserve quantity must not exceed available quantity!",
            )

        return render(request, self.template_name, {"form": form, "product": product})

    def get_success_url(self, pk):
        """Get success URL after post completion"""

        return reverse("product-details", kwargs={"pk": pk})
