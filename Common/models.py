from django.db import models


# TODO - [] make upload_to dynamic
# TODO - [] implement generic FKs?
# TODO - [] clean out code now covered in services.py
# TODO - [] Should I add delete method from services to models?
# TODO - [x] handle alt text for images
# TODO - [x] clean out code now covered in services.py
# TODO - [N] Should I add delete method from services to models?
# TODO - [] Implement signals to further detach logic from views?


class ImageUpload(models.Model):
    file = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.file.name if self.file else "No File"

    @staticmethod
    def validate_image_size_parameter(size):
        # Validate the size parameter is a tuple of length 2
        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError("size parameter must be a tuple of (width, height)")
        # validate size elements are positive integers
        if not all(isinstance(n, int) and n > 0 for n in size):
            raise ValueError("size must contain positive integers")


class ProductImage(ImageUpload):
    related_model = models.ForeignKey(
        "Products.Product", related_name="image", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.related_model.name} image"
