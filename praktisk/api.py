from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import InfoPage

api_router = WagtailAPIRouter("praktiskapi")


class InfoPagesAPIViewSet(PagesAPIViewSet):
    model = InfoPage
    renderer_classes = [
        JSONRenderer,
    ]


if settings.DEBUG:
    InfoPagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router.register_endpoint("info", InfoPagesAPIViewSet)
