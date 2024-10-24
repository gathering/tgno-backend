from django.conf import settings
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet

# "Base" routes
# Content/app specific routes existing in each individual app, not here


class AppImagesAPIViewSet(ImagesAPIViewSet):
    # To disable rest_framework's default browsable renderer
    # - https://github.com/wagtail/wagtail/issues/6066
    #   (outlines how they secretly ignore/override default REST_FRAMEWORK config options)
    # - https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html#enable-the-app
    #   (says rest_framework is optional, it isn't)
    renderer_classes = [
        JSONRenderer,
    ]


if settings.DEBUG:
    AppImagesAPIViewSet.renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("images", AppImagesAPIViewSet)
