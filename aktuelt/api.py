from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import NewsPage

api_router = WagtailAPIRouter("aktueltapi")


class NewsPagesAPIViewSet(PagesAPIViewSet):
    model = NewsPage

    meta_fields = PagesAPIViewSet.meta_fields + ["last_published_at"]

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

print(NewsPagesAPIViewSet.renderer_classes)
api_router.register_endpoint("news", NewsPagesAPIViewSet)
