from django.db import models
from schedule.models import Event as EventBase
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase
from wagtail.fields import RichTextField


# We use tag instead of category to allow used of hidden "meta" tags (ex. "featured")
# most of the time we expect an event to only have one regular tag
class Tag(TagBase):
    free_tagging = False
    hidden = models.BooleanField(default=False)
    type = models.CharField(
        choices=[
            ("category", "Category"),
            ("location", "Location"),
            ("meta", "Meta"),
        ],
        default="category",
        max_length=10,
    )
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class EventTag(TaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="event_tags",
    )

    content_object = models.ForeignKey("program.Event", on_delete=models.CASCADE)


class Event(EventBase, models.Model):
    tags = TaggableManager(through=EventTag, blank=True)
    hidden = models.BooleanField(default=False)
    related_page = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE, null=True, blank=True)
    related_url = models.URLField(blank=True)
