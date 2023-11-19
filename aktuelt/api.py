from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import NewsPage

api_router = WagtailAPIRouter("aktueltapi")


class NewsPagesAPIViewSet(PagesAPIViewSet):
    model = NewsPage


api_router.register_endpoint("news", NewsPagesAPIViewSet)
