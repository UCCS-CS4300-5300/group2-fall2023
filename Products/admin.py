# Django admin file for Products app
# allows for admin to edit products

from django.contrib import admin
from .models import Product

admin.site.register(Product)
