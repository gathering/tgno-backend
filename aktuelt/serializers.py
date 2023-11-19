from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField


class AuthorsSerializer(Field):
    def to_representation(self, value):
        return [
            {
                "id": value.id,
                "name": value.name,
                "image": ImageRenditionField("fill-100x100").to_representation(value.author_image)
                if value.author_image
                else None,
            }
            for value in value.all()
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
