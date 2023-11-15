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
from django.core.exceptions import PermissionDenied

from .models import Product
from .forms import ProductForm, ProductReserveForm
from Common.forms import ProductImageForm
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
    image_form_class = ProductImageForm

    # Establish the target template for use
    template_name = "product_create.html"

    def form_valid(self, form):
        """Update the `owner` field after submission"""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        if self.image_form and self.image_form.is_valid():
            image = self.image_form.save(commit=False)
            image.product = self.object
            image.save()

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

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if "file" in request.FILES:
            self.image_form = self.image_form_class(request.POST, request.FILES)
        else:
            self.image_form = None

        if form.is_valid() and (self.image_form is None or self.image_form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form, self.image_form)


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
    image_form_class = ProductImageForm

    # Establish the target template for use
    template_name = "product_update.html"

    def form_valid(self, form):
        self.object = form.save()

        self.handle_image_update()

        return super().form_valid(form)

    def get(self, request, pk):
        """Handle get request to delete product"""

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can get the form
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        form = self.form_class(instance=product)
        return render(request, self.template_name, {"form": form, "product": product})

    def post(self, request, pk):
        """Handle post request"""

        product = get_object_or_404(Product, pk=pk)
        form = self.form_class(request.POST, instance=product)

        # Only the Product's owner can get the form
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            form = self.form_class(instance=product)

        return render(request, self.template_name, {"form": form, "product": product})

    def get_success_url(self):
        """Get success URL after post completion."""

        return reverse("product-details", kwargs={"pk": self.get_object().pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        self.image_form = self.image_form_class(
            request.POST, request.FILES, instance=self.get_image_instance()
        )

        if form.is_valid() and self.image_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, self.image_form)

    def handle_image_update(self):
        if self.image_form and self.image_form.is_valid():
            file = self.image_form.cleaned_data.get("file")
            alt_text = self.image_form.cleaned_data.get("alt_text")
            print("file:", file)
            if file:
                product_image, created = ProductImage.objects.update_or_create(
                    product=self.object, defaults={"file": file, "alt_text": alt_text}
                )
            elif not file:
                print("Deleting ProductImage:", self.image_form.instance)
                ProductImage.objects.filter(product=self.object).delete()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        self.image_form = self.image_form_class(
            request.POST, request.FILES, instance=self.get_image_instance()
        )

        if form.is_valid() and self.image_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, self.image_form)

    def handle_image_update(self):
        if self.image_form and self.image_form.is_valid():
            file = self.image_form.cleaned_data.get("file")
            alt_text = self.image_form.cleaned_data.get("alt_text")
            print("file:", file)
            if file:
                product_image, created = ProductImage.objects.update_or_create(
                    product=self.object, defaults={"file": file, "alt_text": alt_text}
                )
            elif not file:
                print("Deleting ProductImage:", self.image_form.instance)
                ProductImage.objects.filter(product=self.object).delete()


class ProductDelete(LoginRequiredMixin, DeleteView):
    """Delete a specific product. URL `/products/delete/<int:pk>/`"""

    # Establish the model type and template name for the generic view
    model = Product
    template_name = "product_delete.html"

    def get(self, request, pk):
        """Handle get request to delete product"""

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can access the page
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        return render(request, self.template_name, {"product": product})

    def post(self, request, pk):
        """Handle post request"""

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can create the object
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        product.delete()
        return HttpResponseRedirect(self.get_success_url())

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
