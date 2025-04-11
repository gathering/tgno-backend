from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.models import Page

from .models import HomePage

# from home.serializers import HomePageSerializer


api_router = WagtailAPIRouter("homeapi")


class HomePagesAPIViewSet(PagesAPIViewSet):
    renderer_classes = [
        JSONRenderer,
    ]

    # serializer_class = HomePageSerializer

    meta_fields = PagesAPIViewSet.meta_fields + ["url"]

    def get_base_queryset(self):
        # Only allow page types we own, and that are live
        return Page.objects.all().type(HomePage).live()


if settings.DEBUG:
    HomePagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router.register_endpoint("home", HomePagesAPIViewSet)
