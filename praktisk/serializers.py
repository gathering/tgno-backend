from rest_framework.fields import Field
from wagtail.api.v2.serializers import PageSerializer

from aktuelt.serializers import NewsBodySerializer


class FaqChildPageSerializer(Field):
    def to_representation(self, pages):
        return [
            {
                "id": entry.id,
                "title": entry.title,
                "url": entry.url,
                "body": NewsBodySerializer().to_representation(entry.body),
            }
            for entry in pages.all()
        ]


class InfoChildPageSerializer(PageSerializer):
    def to_representation(self, pages):
        return [
            {
                "id": entry.id,
                "title": entry.title,
                "url": entry.url,
                "intro": entry.body,
            }
            for entry in pages.all()
        ]
