from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField


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


class NewsPageGallerySerializer(Field):
    def to_representation(self, value):
        return [
            # 100% guarantee there are better ways to do this
            # TODO: Replace with generic and reusable serializer
            ImageRenditionField("fill-100x100").to_representation(gallery_image.image)
            for gallery_image in value.all()
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
