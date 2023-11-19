from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Orderable, Page, forms
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from aktuelt.serializers import (
    AuthorsSerializer,
    NewsPageGallerySerializer,
    NewsPageTagsSerializer,
)


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey("NewsPage", related_name="tagged_items", on_delete=models.CASCADE)


class NewsTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        newspages = NewsPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["newspages"] = newspages
        return context


class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        newspages = self.get_children().live().order_by("-first_published_at")
        context["newspages"] = newspages
        return context


class NewsPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField("aktuelt.Author", blank=True)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()

        return gallery_item.image if gallery_item else None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    api_fields = [
        APIField("intro"),
        APIField("body"),
        APIField("date"),
        # TODO: Replace with prettier (main model based?) serializer pattern?
        APIField("authors", serializer=AuthorsSerializer()),
        APIField("tags", serializer=NewsPageTagsSerializer()),
        APIField("gallery_images", serializer=NewsPageGallerySerializer()),
        APIField("main_image", serializer=ImageRenditionField("fill-100x100")),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                FieldPanel("tags"),
            ],
            heading="News information",
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]


class NewsPageGalleryImage(Orderable):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"
