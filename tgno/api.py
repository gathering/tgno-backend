from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet

# "Base" routes
# Content/app specific routes existing in each individual app, not here

api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("images", ImagesAPIViewSet)
