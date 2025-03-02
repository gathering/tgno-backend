from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from aktuelt.api import api_router as aktuelt_api_router
from praktisk.api import api_router as praktisk_api_router
from program.api import urlpatterns as program_urls
from search import views as search_views

from .api import api_router as base_api_router

urlpatterns = [
    path(r"backend-health/", include("health_check.urls")),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("", include("social_django.urls")),
    path("api/v2/documents/", include(wagtaildocs_urls)),
    path("api/v2/search/", search_views.search, name="search"),
    path("api/v2/", base_api_router.urls),
    path("api/v2/", aktuelt_api_router.urls),
    path("api/v2/", praktisk_api_router.urls),
    path("api/v2/", include(program_urls)),
    re_path(r"^", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
