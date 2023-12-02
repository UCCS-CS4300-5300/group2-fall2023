### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Forms

""" Implementation of Common models """

from django import forms
from django.forms import modelform_factory
from PIL import Image as PIL

from Common.models import ProductImage
from Common.services import ImageService

# TODO -[] Check validator methods and update as necessary


class ImageUploadForm(forms.ModelForm):
    """Image upload form information"""

    class Meta:
        """ Image upload form Meta Class """

        fields = ["file", "alt_text"]
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                    "aria-label": "Upload an image",
                }
            ),
            "alt_text": forms.TextInput(
                attrs={
                    "placeholder": "Image description",
                    "aria-label": "Image description",
                }
            ),
        }

        labels = {
            "file": "Image upload",
            "alt_text": "Image description",
        }

        required = {
            "file": False,
            "alt_text": False,
        }

    def clean_file(self):
        """Performs various validations on image file, returning it if valid"""
        file = self.cleaned_data.get("file") or None

        if file is None:
            return None

        # check for valid, non-corrupted image file.
        self.validate_file(file)

        # validate image file size
        self.validate_file_size(file)

        # validate image dimensions (width, height)
        self.validate_image_dimensions(file)

        return file

    @staticmethod
    def validate_file(file):
        """ Validate image file contents, format, max and min size """
        
        # return since image upload is optional
        if not file:
            return

        # validate image file contents
        try:
            with PIL.open(file) as image:
                # check image is valid and readable
                image.verify()
                # check image format is supported
                if image.format not in ImageService.ACCEPTED_FILE_TYPES:
                    raise forms.ValidationError("Invalid file format provided.")
        except Exception:
            raise forms.ValidationError("Invalid file.")

    @staticmethod
    def validate_image_dimensions(image):
        """ Takes an image file and validates its width and height against
            the max allowed as defined in Image model: MAX_IMAGE_SIZE
        """

        if not image:
            return

        try:
            with PIL.open(image) as img:
                max_width, max_height = ImageService.MAX_IMAGE_SIZE
                if img.width > max_width or img.height > max_height:
                    exceeded_dimension = "width" if img.width > max_width else "height"

                    raise forms.ValidationError(
                        f"Image {exceeded_dimension} exceeds maximum allowed. Max allowed is \
                            {ImageService.MAX_IMAGE_SIZE[0]}x{ImageService.MAX_IMAGE_SIZE[1]}"
                    )

        except Exception:
            raise forms.ValidationError("Invalid image file.")

    @staticmethod
    def validate_file_size(file):
        """checks file is not too large or small in size"""

        if not file:
            return

        if file.size > ImageService.MAX_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too large. max size is {ImageService.MAX_FILE_SIZE_MB} MB"
            )

        if file.size < ImageService.MIN_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too small. min size is {ImageService.MIN_FILE_SIZE_KB} KB"
            )


# Dynamic forms for adding images to models

# form factory for products
ProductImageForm = modelform_factory(
    ProductImage, form=ImageUploadForm, fields=["file", "alt_text"]
)
