# https://docs.wagtail.org/en/stable/extending/rich_text_internals.html#rewrite-handlers
from wagtail import hooks

from aktuelt.handlers import CustomImageEmbedHandler


# Higher order to make sure it runs after image handler hook in images app
@hooks.register("register_rich_text_features", order=10)
def register_embed_handler(features):
    features.register_embed_type(CustomImageEmbedHandler)
