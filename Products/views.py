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
from .forms import ProductForm, ReservationForm
from Events.models import Event


from Common.models import ProductImage
from Common.forms import ProductImageForm
from Common.services import ImageService


class ProductList(ListView):
    """ Get a list of Harvestly products. URL `/get-products-list/` """

    # Specify model and template
    model = Product
    template_name = "product_list.html"
    context_object_name = "product_list"


# TODO create new create view, inherit from `View` class


class ProductCreate(LoginRequiredMixin, CreateView):
    """ Create View for an Event Object. URL `/products/new/` """

    # Establish model type and form class for use
    model = Product
    form_class = ProductForm
    image_form_class = ProductImageForm

    # Establish the target template for use
    template_name = "product_create.html"

    def form_valid(self, form):
        """ Update the `owner` field after submission """

        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()

        # if image was uploaded, create image object
        image_file = self.request.FILES.get("file", None)
        if image_file:
            ImageService().create_image(
                image_file,
                product,
                ProductImage,
                resize_to=ImageService.DEFAULT_IMAGE_SIZE,
            )

        return super().form_valid(form)

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """ Include list of events in context data """

        # In order to iterate over the model options, we need to provide the list in
        #   the context. Unfortunately, iterating through Choice Select options is not
        #   supported in this version of Django.

        context = super().get_context_data(**kwargs)
        context["event_list"] = Event.objects.filter(organizer=self.request.user)
        context["image_form"] = self.image_form_class()

        # Set initial event ID value (when redirected from event details page, or reload)
        event_id = self.kwargs.get("event_id")
        if event_id:
            context["event_id"] = event_id
            return context

        # Set event id attribute on form resubmission
        f_kwargs = super().get_form_kwargs()
        form_data = f_kwargs.get("data")

        if form_data:
            event_id = form_data.get("product_event")

            if event_id:
                context["event_id"] = event_id

        return context


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
    image_form_class = ProductImageForm

    # Establish the target template for use
    template_name = "product_update.html"

    def get(self, request, pk):
        """ Handle get request to update/edit product """

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can get the form
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        form = self.form_class(instance=product)

        # if product has image, use in image form, else blank form.
        image_form = self.image_form_class(instance=product.image.first())

        # include image_form in context
        context = {
            "form": form,
            "product": product,
            "image_form": image_form,
            "event_list": Event.objects.filter(organizer=request.user),
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        """ Handle post request """

        product = get_object_or_404(Product, pk=pk)
        form = self.form_class(request.POST, instance=product)

        # Only the Product's owner can get the form
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        image = product.image.first()
        image_form = self.image_form_class(request.POST, request.FILES, instance=image)

        if form.is_valid() and image_form.is_valid():
            form.save()

            # perform image processing, updating, creating
            if image_form.cleaned_data.get("file") is None and image:
                # product has image instance but no image, delete
                ImageService().delete_image_instance(image)

            else:
                image = ImageService().handle_image_update(
                    image_form.cleaned_data, product, ProductImage
                )

                if image:
                    image_form.save()

            return HttpResponseRedirect(self.get_success_url())

        return render(request, self.template_name, {
            "form": form,
            "image_form": image_form,
            "product": product,
            "event_list": Event.objects.filter(organizer=request.user),
        })

    def get_success_url(self):
        """ Get success URL after post completion. """

        return reverse("product-details", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # find image_Form and add to context
        if "image_form" not in context:
            if self.object.image.exists():
                # image exists, update form
                context["image_form"] = self.image_form_class(
                    instance=self.object.image.first()
                )
            else:
                # no image exists, create new form
                context["image_form"] = self.image_form_class()

        return context


class ProductDelete(LoginRequiredMixin, DeleteView):
    """ Delete a specific product. URL `/products/delete/<int:pk>/` """

    # Establish the model type and template name for the generic view
    model = Product
    template_name = "product_delete.html"

    def get(self, request, pk):
        """ Handle get request to delete product """

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can access the page
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        return render(request, self.template_name, {"product": product})

    def post(self, request, pk):
        """ Handle post request """

        product = get_object_or_404(Product, pk=pk)

        # Only the Product's owner can create the object
        if not request.user.id == product.owner.id:
            raise PermissionDenied()

        product.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Get success URL after post completion """

        return reverse("products")


class ProductReserve(LoginRequiredMixin, View):
    """ Reserve a quantity of a specific product. URL `/products/reserve/<int:pk>/` """

    template_name = "product_reserve.html"

    def get(self, request, pk):
        """ Handle get request to view (render form) """

        product = get_object_or_404(Product, pk=pk)
        form = ReservationForm

        return render(request, self.template_name, {"form": form, "product": product})

    def post(self, request, pk):
        """ Handle post request """

        product = get_object_or_404(Product, pk=pk)
        form = ReservationForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            if quantity <= product.quantity:
                product.quantity -= quantity
                product.save()

                reservation = form.save(commit=False)
                reservation.customer = self.request.user
                reservation.product = product
                reservation.save()

                return HttpResponseRedirect(self.get_success_url(pk))

            form.add_error("quantity", "Reserve quantity must not exceed available quantity!")

        return render(request, self.template_name, {"form": form, "product": product})

    def get_success_url(self, pk):
        """ Get success URL after post completion """

        return reverse("product-details", kwargs={"pk": pk})
