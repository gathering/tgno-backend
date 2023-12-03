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

    def get_queryset(self):
        allowed_models = [InfoIndexPage, InfoPage]
        return super().get_queryset().type(tuple(allowed_models))


api_router.register_endpoint("info", InfoPagesAPIViewSet)
