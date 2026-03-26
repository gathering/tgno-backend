from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.models import Page

from .models import Competition, CompetitionCategoryPage

api_router = WagtailAPIRouter("konkurranseapi")


class CompetitionAPIViewSet(PagesAPIViewSet):
    """API endpoint for competition pages"""

    renderer_classes = [
        JSONRenderer,
    ]

    meta_fields = PagesAPIViewSet.meta_fields + [
        "first_published_at",
        "last_published_at",
    ]

    def get_base_queryset(self):
        # Only return Competition and CompetitionCategoryPage types that are live
        return Page.objects.all().type(Competition, CompetitionCategoryPage).live()


if settings.DEBUG:
    CompetitionAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router.register_endpoint("competitions", CompetitionAPIViewSet)
