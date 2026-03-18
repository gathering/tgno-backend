from django.urls import path

from .views_preview import news_frontend_preview

urlpatterns = [
    path("preview/news/<str:token>/", news_frontend_preview, name="news_frontend_preview"),
]
