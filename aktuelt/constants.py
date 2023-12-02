from django.db import models


class ContributionTypes(models.TextChoices):
    # TODO: Localization? Can we store the constant and translate to norwegian when shown to the user?
    # Ref:
    # - https://docs.djangoproject.com/en/4.2/ref/models/fields/#enumeration-types
    # - https://docs.wagtail.org/en/stable/advanced_topics/i18n.html#internationalisation
    TEXT = "Text"
    PHOTOGRAPHY = "Photography"
    VIDEO = "Video"
    AUDIO = "Audio"
    OTHER = "Other"
