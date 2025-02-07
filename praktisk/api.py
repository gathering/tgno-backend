from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.models import Page

from .models import FaqPage, InfoPage

api_router = WagtailAPIRouter("praktiskapi")


class InfoPagesAPIViewSet(PagesAPIViewSet):
    renderer_classes = [
        JSONRenderer,
    ]

    meta_fields = PagesAPIViewSet.meta_fields + ["url"]

    def get_listing_default_fields(self):
        return [
            "body",
            "intro",
            "id",
            "slug",
            "title",
            "type",
            "url",
        ]

    def get_base_queryset(self):
        # Only allow page types we own
        return Page.objects.all().type(InfoPage, FaqPage)


if settings.DEBUG:
    InfoPagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router.register_endpoint("info", InfoPagesAPIViewSet)
