from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # image = models.ImageField(upload_to='products/images') # need pillow installed
    product_vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name