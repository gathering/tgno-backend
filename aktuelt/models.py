from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from aktuelt.constants import ContributionTypes
from aktuelt.serializers import (
    ContributorsSerializer,
    NewsBodySerializer,
    NewsPageTagsSerializer,
)
from home.serializers import ImageSerializer


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey("NewsPage", related_name="tagged_items", on_delete=models.CASCADE)


class NewsTagIndexPage(Page):
    page_description = "Page to list all published news items with given tag"

    def get_context(self, request):
        tag = request.GET.get("tag")
        newspages = NewsPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["newspages"] = newspages
        return context


class NewsIndexPage(Page):
    page_description = "Page to list all published news items"
    subpage_types = ["aktuelt.NewsPage"]

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        newspages = self.get_children().live().order_by("-first_published_at")
        context["newspages"] = newspages
        return context


class NewsPage(Page):
    page_description = "A regular news page"
    parent_page_types = ["aktuelt.NewsIndexPage"]
    subpage_types = []

    custom_published_at = models.DateTimeField("Publish override", blank=True, null=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    main_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    api_meta_fields = [
        "custom_published_at",
    ]

    api_fields = [
        APIField("intro"),
        APIField("body", serializer=NewsBodySerializer()),
        # TODO: Replace with prettier (main model based?) serializer pattern?
        APIField("contributors", serializer=ContributorsSerializer(source="news_page_contributors")),
        APIField("tags", serializer=NewsPageTagsSerializer()),
        APIField("main_image", serializer=ImageSerializer()),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("main_image"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("custom_published_at"),
                FieldPanel("tags"),
                InlinePanel("news_page_contributors", label="Contributors"),
            ],
            heading="News information",
        ),
    ]


class NewsPageContributor(Orderable):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name="news_page_contributors")
    contributor = models.ForeignKey("aktuelt.Contributor", on_delete=models.CASCADE, related_name="+")
    contribution_type = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("contributor"),
        FieldPanel("contribution_type"),
    ]


@register_snippet
class Contributor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    default_contribution_type = models.CharField(
        max_length=250, choices=ContributionTypes.choices, default=ContributionTypes.TEXT
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("default_contribution_type"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contributors"
