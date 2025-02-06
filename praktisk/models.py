from wagtail.api.v2.views import APIField
from wagtail.models import Page


# Basic "static" information page that can be endlessly nested
class InfoPage(Page):
    page_description = "A regular info page"
    parent_page_types = ["home.HomePage", "praktisk.InfoPage"]
    subpage_types = ["praktisk.InfoPage", "praktisk.FaqIndexPage"]

    api_meta_fields = [
        APIField("url"),
    ]


# Information snippets that only exists as siblings of each other
class FaqPage(Page):
    page_description = "A regular FAQ entry page"
    parent_page_types = ["praktisk.FaqIndexPage"]
    subpage_types = []


# Page to display a collection of FAQ items
class FaqIndexPage(Page):
    page_description = "Page to list FAQ items"
    subpage_types = ["praktisk.FaqPage"]

    api_meta_fields = [
        APIField("url"),
    ]
