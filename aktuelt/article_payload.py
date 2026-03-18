from __future__ import annotations

from typing import Any

from aktuelt.serializers import (
    ContributorsSerializer,
    NewsBodySerializer,
    NewsImageSerializer,
    NewsPageTagsSerializer,
)


def build_news_article_payload(page) -> dict[str, Any]:
    """
    Build the exact JSON shape the Astro frontend consumes for news articles.

    Kept as a shared helper so both preview and any future endpoints can reuse it.
    """
    return {
        "id": page.id,
        "title": page.title,
        "intro": page.intro,
        "body": NewsBodySerializer().to_representation(page.body),
        "contributors": ContributorsSerializer().to_representation(page.news_page_contributors),
        "tags": NewsPageTagsSerializer().to_representation(page.tags),
        "main_image": NewsImageSerializer().to_representation(page.main_image) if page.main_image else None,
        "meta": {
            "type": "aktuelt.NewsPage",
            "detail_url": None,
            "html_url": None,
            "slug": page.slug,
            "first_published_at": page.first_published_at.isoformat() if page.first_published_at else None,
            "custom_published_at": page.custom_published_at.isoformat() if page.custom_published_at else None,
            "seo_title": page.seo_title,
            "search_description": page.search_description,
            "locale": getattr(page.locale, "language_code", None),
        },
    }
