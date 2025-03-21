from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.images.models import Image as WagtailImage
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class CustomImage(AbstractImage):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")
    uncroppable = models.BooleanField(default=False)

    admin_form_fields = WagtailImage.admin_form_fields + ("uncroppable",)

    class Meta(AbstractImage.Meta):
        verbose_name = "image"
        verbose_name_plural = "images"
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class CustomRendition(AbstractRendition):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
