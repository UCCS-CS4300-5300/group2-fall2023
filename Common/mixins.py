from django.forms import ModelForm
from django.shortcuts import redirect
from django.urls import reverse
from .models import ImageUpload, ProductImage
from .forms import ImageUploadForm


class ImageHandlingMixin:
    image_form_class = None

    def get_image_instance(self):
        # to be overridden in views as needed
        raise NotImplementedError(
            "get_image_instance() must be overridden in a subclass"
        )

    def create_image_form(
        self,
        request,
    ):
        pass

    def handle_image_form(self, model_instance, image_form):
        # to be overridden in views as needed
        raise NotImplementedError(
            "handle_image_form() must be overridden in a subclass"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "image_form" not in context:
            image_instance = self.get_image_instance()
            context["image_form"] = self.image_form_class(instance=image_instance)
        return context

    def get_image_instance(self):
        if self.object and hasattr(self.object, "image"):
            image_instance = self.object.image.first()
            return image_instance.image if image_instance else None
        return None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if hasattr(self, "get_object") else None
        form = self.get_form()
        image_form = self.image_form_class(
            request.POST, request.FILES, instance=self.get_image_instance()
        )

        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        self.object = form.save()
        image = image_form.save(commit=False)
        image.related_object = self.object
        image.save()
        return super(ImageHandlingMixin, self).form_valid(form)

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )
