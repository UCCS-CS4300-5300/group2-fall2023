### CS 4300 Fall 2023 Group 2
### Harvestly
### Reservations Views

""" Implementation of Reservation Create, Update, and Delete Views """

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404

from Products.models import Product
from Reservations.models import Reservation
from Reservations.forms import ReservationForm


class ReservationCreate(LoginRequiredMixin, CreateView):
    """ Reserve a quantity of a specific product. URL `/reservations/new/` """

    model = Reservation
    form_class = ReservationForm
    template_name = "reservation_create.html"

    def get(self, request, product_id):
        """ Handle Get Request """

        product = get_object_or_404(Product, pk=product_id)
        form = self.get_form()

        # Product owner cannot reserve
        if request.user.id == product.owner.id:
            raise PermissionDenied()

        return render(request, self.template_name, {
            "form": form,
            "product": product,
        })

    def post(self, request, product_id):
        """ Handle Post request """

        product = get_object_or_404(Product, pk=product_id)
        form = self.get_form()

        # Product owner cannot reserve
        if request.user.id == product.owner.id:
            raise PermissionDenied()

        if form.is_valid():
            reserve_quantity = form.cleaned_data["quantity"]

            # Add form error if reserve quantity exceeds available quantity
            if reserve_quantity > product.quantity:
                form.add_error("quantity", "Reserve quantity must not exceed product quantity!")

            else:
                # Set reservation customer, product, and price, and return success
                product_price = product.price
                quantity = form.instance.quantity

                form.instance.customer = self.request.user
                form.instance.product = Product.objects.get(pk=product_id)
                form.instance.price = product_price * quantity

                return self.form_valid(form)

        return render(request, self.template_name, {
            "form": form,
            "product": product,
        })

    def get_success_url(self):
        """ Get success URL after post completion. """

        product_id = self.kwargs.get("product_id")

        if not product_id:
            raise Http404()

        return reverse("product-details", kwargs={"pk": product_id})


class ReservationUpdate(LoginRequiredMixin, UpdateView):
    """ Reservation Update View """

    model = Reservation
    form_class = ReservationForm
    template_name = "reservation_update.html"

    def get(self, request, pk):
        """ Handle Get Request """

        reservation = get_object_or_404(Reservation, pk=pk)

        # Only the reservation customer can access the form
        if not request.user.id == reservation.customer.id:
            raise PermissionDenied()

        form = self.form_class(instance=reservation)

        return render(request, self.template_name, {
            "form": form,
            "reservation": reservation,
            "product": reservation.product
        })

    def post(self, request, pk):
        """ Handle Post Request """

        reservation = get_object_or_404(Reservation, pk=pk)
        form = self.form_class(request.POST, instance=reservation)

        # Only the reservation customer can access the page
        if not request.user.id == reservation.customer.id:
            raise PermissionDenied()

        if form.is_valid():
            reserve_quantity = form.cleaned_data["quantity"]

            # Add form error if reserve quantity exceeds available quantity
            if reserve_quantity > reservation.product.quantity:
                form.add_error("quantity", "Reserve quantity must not exceed product quantity!")

            else:
                # Set reservation customer, product, and price, and return success
                reservation.price = form.instance.quantity * reservation.product.price
                form.save()

                # Go back to the details page for the reserved product
                return redirect(reverse("product-details", kwargs={"pk": reservation.product.id}))

        return render(request, self.template_name, {
            "form": form,
            "reservation": reservation,
            "product": reservation.product,
        })


class ReservationDelete(LoginRequiredMixin, DeleteView):
    """ Reservation Delete View """

    model = Reservation
    template_name = "reservation_delete.html"

    def get(self, request, pk):
        """ Handle get request to delete product """

        reservation = get_object_or_404(Reservation, pk=pk)

        # Only the Product's owner can access the page
        if not request.user.id == reservation.customer.id:
            raise PermissionDenied()

        return render(request, self.template_name, {"reservation": reservation})

    def post(self, request, pk):
        """ Handle post request """

        reservation = get_object_or_404(Reservation, pk=pk)

        # Only the Product's owner can create the object
        if not request.user.id == reservation.customer.id:
            raise PermissionDenied()

        reservation.delete()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """ Get success URL after post completion """

        return reverse("cart")
