from django.shortcuts import redirect
from django.urls import reverse
from django.forms import ModelForm
from .models import ImageUpload, ProductImage
from .forms import ImageUploadForm


class ImageHandlingMixin:
    image_form_class = None

    def get_image_instance(self):
        """Gets relevant class instance for image"""
        if self.object is None or not hasattr(self.object, "image"):
            return None
        return self.object.image.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "image_form" not in context:
            image_instance = self.get_image_instance()
            context["image_form"] = self.image_form_class(instance=image_instance)
        return context

    def form_valid(self, form):
        if self.image_form and self.image_form.is_valid():
            self.object = form.save()
            image = self.image_form.save(commit=False)
            image.related_object = self.object
            image.save()
        return super(ImageHandlingMixin, self).form_valid(form)

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )
