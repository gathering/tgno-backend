from django.conf import settings


def get_site_info(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "KEYCLOAK_LOGIN": settings.SOCIAL_AUTH_KEYCLOAK_KEY is not None,
        "DISABLE_LOCAL_AUTH": settings.DISABLE_LOCAL_AUTH,
    }
