from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField
from wagtail.rich_text import expand_db_html


class NewsBodySerializer(Field):
    def to_representation(self, value):
        return expand_db_html(value)


class ContributorsSerializer(Field):
    def to_representation(self, news_page_contributors):
        return [
            {
                "id": entry.contributor.id,
                "name": entry.contributor.name,
                "contribution_type": entry.contribution_type or entry.contributor.default_contribution_type,
                "image": ImageRenditionField("fill-100x100").to_representation(entry.contributor.image)
                if entry.contributor.image
                else None,
            }
            for entry in news_page_contributors.all()
        ]


class NewsPageTagsSerializer(Field):
    def to_representation(self, value):
        return [
            {
                "id": tag.id,
                "name": tag.name,
                "slug": tag.slug,
            }
            for tag in value.all()
        ]
