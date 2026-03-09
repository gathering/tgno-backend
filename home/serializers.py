from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField


class ImageSerializer(Field):
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
            "uncroppable": value.uncroppable if getattr(value, "uncroppable") else False,
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
