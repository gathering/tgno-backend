from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def news_frontend_preview(request, token: str):
    payload = cache.get(f"news_preview:{token}")
    if payload is None:
        return JsonResponse({"detail": "Preview token not found or expired."}, status=404)

    response = JsonResponse(payload)

    # Allow the frontend origin to fetch this endpoint during preview.
    # (We intentionally keep this narrow and opt-in.)
    frontend_origin = getattr(settings, "FRONTEND_PREVIEW_ORIGIN", None)
    if frontend_origin:
        response["Access-Control-Allow-Origin"] = frontend_origin
        response["Vary"] = "Origin"

    return response
