from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField


class NewsImageSerializer(Field):
    def image_size(self, size, value):
        image = ImageRenditionField(size).to_representation(value)
        return {"url": image["full_url"], "width": image["width"], "height": image["height"]}

    def to_representation(self, value):
        data = {
            "id": value.id,
            "title": value.title,
            "alt": value.title,
            "type": "foto",
            "focus": "center",
            "author": None,
            "sizes": {
                "thumbnail": self.image_size("fill-150x150", value),
                "small": self.image_size("max-300x300", value),
                "medium": self.image_size("max-700x700", value),
                "large": self.image_size("max-1600x1600", value),
                "extra_large": self.image_size("max-3200x3200", value),
            },
        }
        data["url"] = data["sizes"]["large"]["url"]
        return data


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
            NewsImageSerializer().to_representation(gallery_image.image)
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
