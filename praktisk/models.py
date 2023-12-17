from django.db import models
from rest_framework.serializers import ModelSerializer
from wagtail.api.v2.serializers import (
    BaseSerializer,
    ChildRelationField,
    Field,
    get_serializer_class,
)
from wagtail.api.v2.views import APIField, PageSerializer

from aktuelt.models import NewsIndexPage, NewsPage
from praktisk.serializers import ChildInfoIndexPagesSerializer, ChildInfoPageSerializer

# In info context we imagine structures like this
# - Practical info (top index/intro) - InfoIndexPage
#   - Standalone info page 1 - InfoPage
#   - Safety info (topic intro) - InfoPageIndex
#     - Safety page 1 - InfoPage
#     - Safety page 2 - InfoPage
#   - ...
#   - Ticket info (topic intro) - InfoPageIndex
#    - Ticket page 1 - InfoPage
#    - ...
#
# This is a bit different from the news context, where we mostly organize based
# on tags. This initial setup is an assumption, so feel free to adjust as needed.


# Extending the NewsPage models since they have a lot of similarities,
# feel free to split them up when/if conventient
class InfoPage(NewsPage):
    page_description = "A regular info page"
    parent_page_types = ["praktisk.InfoIndexPage"]
    subpage_types = []


class InfoIndexPage(NewsIndexPage):
    page_description = "Page to list all published info items"
    parent_page_types = ["home.HomePage", "praktisk.InfoIndexPage"]
    subpage_types = ["praktisk.InfoPage", "praktisk.InfoIndexPage"]

    api_meta_fields = [
        APIField("pages", ChildRelationField(serializer_class=ChildInfoPageSerializer)),
        APIField("topics", serializer=ChildInfoIndexPagesSerializer()),
    ]

    def pages(self):
        return InfoPage.objects.live().descendant_of(self)

    def topics(self):
        return InfoIndexPage.objects.live().descendant_of(self)
