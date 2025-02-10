from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api.v2.views import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page

from aktuelt.serializers import NewsBodySerializer
from praktisk.serializers import FaqChildPageSerializer, InfoChildPageSerializer


# Basic "static" information page that can be endlessly nested
class InfoPage(Page):
    page_description = "A regular info page"
    parent_page_types = ["home.HomePage", "praktisk.InfoPage"]
    subpage_types = ["praktisk.InfoPage", "praktisk.FaqPage"]

    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)

    api_meta_fields = [
        APIField("url"),
    ]

    api_fields = [
        APIField("intro"),
        APIField("body", serializer=NewsBodySerializer()),
        APIField("faq", serializer=FaqChildPageSerializer(source="get_child_faq_pages")),
        APIField("pages", serializer=InfoChildPageSerializer(source="get_child_info_pages")),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    @property
    def get_child_faq_pages(self):
        return FaqPage.objects.child_of(self).live()

    @property
    def get_child_info_pages(self):
        return InfoPage.objects.child_of(self).live()


# Information snippets that only exists as siblings of each other
class FaqPage(Page):
    page_description = "A regular FAQ entry page"
    parent_page_types = ["praktisk.InfoPage"]
    subpage_types = []

    body = RichTextField(blank=True)

    api_meta_fields = [
        APIField("url"),
    ]

    api_fields = [
        APIField("body", serializer=NewsBodySerializer()),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
