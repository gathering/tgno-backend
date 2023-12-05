from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import NewsPage

api_router = WagtailAPIRouter("aktueltapi")


class NewsPagesAPIViewSet(PagesAPIViewSet):
    model = NewsPage

    meta_fields = PagesAPIViewSet.meta_fields + ["last_published_at"]


api_router.register_endpoint("news", NewsPagesAPIViewSet)
