### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Forms

from django import forms
from Common.models import ImageUpload
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
        model = ImageUpload
        fields = ["image", "alt_text"]
        widgets = {
            "image": forms.ClearableFileInput(
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
            "image": "Image",
            "alt_text": "Image description",
        }

    def clean_image(self):
        """Performs various validations on image file, returning it if valid"""
        image = self.cleaned_data.get("image")

        if image is None:
            return image

        # validate image file size
        self.validate_image(image)

        # validate image file size
        self.validate_file_size(image)

        # validate image dimensions (width, height)
        self.validate_image_dimensions(image)

        return image

    @staticmethod
    def validate_image(image):
        """validate image file contents, format, max and min size"""
        # return since image upload is optional
        if not image:
            return

        # validate image file contents
        try:
            with PIL.open(image) as img:
                # check image is valid and readable
                img.verify()
                # check image format is supported
                if img.format not in ACCEPTED_FILE_TYPES:
                    raise forms.ValidationError("Invalid image file format.")
        except Exception as e:
            raise forms.ValidationError("Invalid image file.")

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
    def validate_file_size(image):
        if not image:
            return

        max_in_mb = MAX_FILE_SIZE / 1000000
        min_in_kb = MIN_FILE_SIZE / 1000

        if image.size > MAX_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too large. max size is {max_in_mb} MB"
            )
        elif image.size < MIN_FILE_SIZE:
            raise forms.ValidationError(
                f"Image file too small. min size is {min_in_kb} KB"
            )
