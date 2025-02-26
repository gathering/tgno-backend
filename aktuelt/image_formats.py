# Ref: https://docs.wagtail.org/en/stable/advanced_topics/images/changing_rich_text_representation.html
from django.utils.html import format_html
from wagtail.images.formats import Format, register_image_format


class InlineNewsImageFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        default_html = super().image_to_html(image, alt_text, extra_attributes)

        return format_html("<div>{}<figcaption>{}</figcaption></div>", default_html, alt_text)


register_image_format(
    InlineNewsImageFormat("inline_news_image", "Inline news image", "image-classes object-contain", "max-3200x3200")
)
