### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Forms

""" Implementation of Common models """

from django import forms
from django.forms import modelform_factory

from Common.models import ProductImage
from Common.utils import validate_file, \
    validate_image_dimensions, \
    validate_file_size

class ImageUploadForm(forms.ModelForm):
    """Image upload form information"""

    class Meta:
        """ Image upload form Meta Class """

        model = ProductImage
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

        file = self.cleaned_data.get("file")

        if not file:
            return None

        # check for valid, non-corrupted image file.
        valid_file = validate_file(file)
        if not valid_file[0]:
            raise forms.ValidationError(valid_file[1])

        # validate image file size
        valid_file_size = validate_file_size(file)
        if not valid_file_size[0]:
            raise forms.ValidationError(valid_file_size[1])

        # validate image dimensions (width, height)
        valid_image_dimensions = validate_image_dimensions(file)
        if not valid_image_dimensions[0]:
            raise forms.ValidationError(valid_image_dimensions[1])

        return file

ProductImageForm = modelform_factory(
    ProductImage, form=ImageUploadForm, fields=["file", "alt_text"]
)
