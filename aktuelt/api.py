from django.conf import settings
from django.db.models.aggregates import Coalesce
from rest_framework.filters import BaseFilterBackend
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import NewsPage

api_router = WagtailAPIRouter("aktueltapi")


class FallbackOrderingFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Try to avoid conflicts with default `OrderingFilter` and `SearchFilter`
        # ie. only apply our sane defaults for non ordered requests
        if "order" in request.GET or "search" in request.GET:
            return queryset

        return queryset.order_by(Coalesce("custom_published_at", "first_published_at").desc(nulls_last=True))


class NewsPagesAPIViewSet(PagesAPIViewSet):
    model = NewsPage

    filter_backends = PagesAPIViewSet.filter_backends + [
        FallbackOrderingFilter,
    ]

    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        "custom_published_at",
    ]

    # To disable rest_framework's default browsable renderer
    # - https://github.com/wagtail/wagtail/issues/6066
    #   (outlines how they secretly ignore/override default REST_FRAMEWORK config options)
    # - https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html#enable-the-app
    #   (says rest_framework is optional, it isn't)
    renderer_classes = [
        JSONRenderer,
    ]


if settings.DEBUG:
    NewsPagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router.register_endpoint("news", NewsPagesAPIViewSet)
