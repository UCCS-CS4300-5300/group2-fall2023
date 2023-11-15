### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Forms

from django import forms
from django.forms import modelform_factory
from Common.models import ProductImage
from Common.models import (
    MAX_IMAGE_SIZE,
    ACCEPTED_FILE_TYPES,
    MAX_FILE_SIZE,
    MIN_FILE_SIZE,
)

from PIL import Image as PIL


class ImageUploadForm(forms.ModelForm):
    """Image upload form information"""

    class Meta:
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
            "file": "Upload File",
            "alt_text": "Image description",
        }

    def save(self, commit=True):
        """Override save method to perform additional actions"""
        instance = super().save(commit=False)

        if not self.cleaned_data["file"] and instance.id:
            if instance.file:
                instance.file.delete(save=False)
            if instance.thumbnail:
                instance.thumbnail.delete(save=False)

        if commit:
            instance.save()
        return instance

    def clean_file(self):
        """Performs various validations on image file, returning it if valid"""
        file = self.cleaned_data.get("file")

        if file is None:
            return file

        # validate image file size
        self.validate_file(file)

        # validate image file size
        self.validate_file_size(file)

        # validate image dimensions (width, height)
        self.validate_image_dimensions(file)

        return file

    @staticmethod
    def validate_file(file):
        """validate image file contents, format, max and min size"""
        # return since image upload is optional
        if not file:
            return

        # validate image file contents
        try:
            with PIL.open(file) as image:
                # check image is valid and readable
                image.verify()
                # check image format is supported
                if image.format not in ACCEPTED_FILE_TYPES:
                    raise forms.ValidationError("Invalid file format provided.")
        except Exception as e:
            raise forms.ValidationError("Invalid file.")

    @staticmethod
    def validate_image_dimensions(image):
        """takes an image file and validates its width and height against the max allowed as defined in Image model: MAX_IMAGE_SIZE"""

        if not image:
            return

        try:
            with PIL.open(image) as img:
                max_width, max_height = MAX_IMAGE_SIZE
                if img.width > max_width or img.height > max_height:
                    exceeded_dimension = "width" if img.width > max_width else "height"

                    raise forms.ValidationError(
                        f"Image {exceeded_dimension} exceeds maximum allowed.  Max allowed is {MAX_IMAGE_SIZE[0]}x{MAX_IMAGE_SIZE[1]}"
                    )
        except Exception as e:
            raise forms.ValidationError("Invalid image file.")

    @staticmethod
    def validate_file_size(file):
        if not file:
            return

        max_in_mb = MAX_FILE_SIZE / 1000000
        min_in_kb = MIN_FILE_SIZE / 1000

        if file.size > MAX_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too large. max size is {max_in_mb} MB"
            )
        elif file.size < MIN_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too small. min size is {min_in_kb} KB"
            )


# Dynamic forms for adding images to models

# for products
ProductImageForm = modelform_factory(
    ProductImage, form=ImageUploadForm, fields=["file", "alt_text"]
)
