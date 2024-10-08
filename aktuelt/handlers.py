# Extends https://github.com/wagtail/wagtail/blob/main/wagtail/images/rich_text/__init__.py#L8
from django.utils.html import escape
from wagtail.images.formats import get_image_format
from wagtail.images.rich_text import ImageEmbedHandler


class CustomImageEmbedHandler(ImageEmbedHandler):
    identifier = "image"

    @classmethod
    def expand_db_attributes_many(cls, attrs_list: list[dict]) -> list[str]:
        """
        Given a dict of attributes from the <embed> tag, return the real HTML
        representation for use on the front-end.
        """
        images = cls.get_many(attrs_list)

        tags = []
        for attrs, image in zip(attrs_list, images):
            if image:
                image_format = get_image_format(attrs["format"])
                tag = image_format.image_to_html(image, attrs.get("alt", ""))
            else:
                tag = '<img alt="">'

            tags.append(tag)

        return tags
