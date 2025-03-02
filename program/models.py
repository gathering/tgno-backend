from django.db import models
from schedule.models import Event as EventBase
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase


# We use tag instead of category to allow used of hidden "meta" tags (ex. "featured")
# most of the time we expect an event to only have one regular tag
class Tag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class EventTag(TaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="event_tags",
    )

    content_object = models.ForeignKey("program.Event", on_delete=models.CASCADE)


class Event(EventBase, models.Model):
    tags = TaggableManager(through=EventTag, blank=True)
