### CS 4300 Fall 2023 Group 2
### Harvestly
### Reservations Views

from typing import Any
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import PermissionDenied

from Products.models import Product
from Reservations.models import Reservation
from Reservations.forms import ReservationForm


class ReservationCreate(LoginRequiredMixin, CreateView):
    """ Reserve a quantity of a specific product. URL `/reservations/new/` """

    model = Reservation
    form_class = ReservationForm
    template_name = "reservation_create.html"

    def get_context_data(self, **kwargs):
        """ Pass product to  template """

        # TODO handle case where product id is null
        # TODO handle case where product does not exist
        product_id = self.kwargs.get("product_id")

        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(pk=product_id)

        return context
    

    def form_valid(self, form):
        """ Update the `customer` and `product` fields after submission """

        # TODO handle case where product id is null
        # TODO handle case where product does not exist
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(pk=product_id)

        product_price = product.price
        quantity = form.instance.quantity

        form.instance.customer = self.request.user
        form.instance.product = Product.objects.get(pk=product_id)
        form.instance.price = product_price * quantity

        return super().form_valid(form)


    def get_success_url(self):
        """ Get success URL after post completion. """

        # TODO handle case where product id is null
        # TODO handle case where product does not exist
        product_id = self.kwargs.get("product_id")

        return reverse("product-details", kwargs={"pk": product_id})


class ReservationUpdate(LoginRequiredMixin, UpdateView):
    """ TODO """
    
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation_update.html"

    # def get(self, request, pk):
    #     """ Handle get request to view (render form) """

    #     product = get_object_or_404(Product, pk=pk)
    #     form = ReservationForm

    #     return render(request, self.template_name, {"form": form, "product": product})



class ReservationDelete(LoginRequiredMixin, DeleteView):
    """ TODO """

    template_name = "reservation_delete.html"
