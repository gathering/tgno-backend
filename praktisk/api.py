from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import InfoIndexPage, InfoPage

api_router = WagtailAPIRouter("praktiskapi")


class InfoPagesAPIViewSet(PagesAPIViewSet):
    # This combined with get_queryset is just an awkward way of only allowing
    # InfoIndexPage and InfoPage to be returned, and not any other page type.
    # Guessing there is a better pattern for this
    known_query_parameters = PagesAPIViewSet.known_query_parameters.difference(["type"])

    meta_fields = PagesAPIViewSet.meta_fields + ["last_published_at"]

    # To disable rest_framework's default browsable renderer
    # - https://github.com/wagtail/wagtail/issues/6066
    #   (outlines how they secretly ignore/override default REST_FRAMEWORK config options)
    # - https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html#enable-the-app
    #   (says rest_framework is optional, it isn't)
    renderer_classes = [
        JSONRenderer,
    ]

    def get_queryset(self):
        allowed_models = [InfoIndexPage, InfoPage]
        return super().get_queryset().type(tuple(allowed_models))


if settings.DEBUG:
    InfoPagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]


api_router.register_endpoint("info", InfoPagesAPIViewSet)
