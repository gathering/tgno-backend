from rest_framework.serializers import ListSerializer, ModelSerializer
from schedule.models import Calendar
from taggit.serializers import TaggitSerializer

from program.models import Event, EventTag, Tag


class EventTagSerializer(ModelSerializer):
    class Meta:
        model = EventTag
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "slug": instance.slug,
            "type": instance.type,
            "hidden": instance.hidden,
            "parent": instance.parent.id if instance.parent else None,
        }


class EventTagsSerializer(ListSerializer):
    child = EventTagSerializer()

    class Meta:
        model = EventTag
        fields = "__all__"


class CalendarSerializer(ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"


class EventSerializer(TaggitSerializer, ModelSerializer):
    cancelled = "cancelled"

    class Meta:
        model = Event
        fields = "__all__"

    def to_representation(self, instance, occurrence=None, extra={}):
        result = {
            "id": instance.id,
            "title": instance.title,
            "tags": EventTagsSerializer().to_representation(instance.tags.filter(hidden=False)),
            "start": instance.start,
            "end": instance.end,
            "description": instance.description,
            "calendar": instance.event.calendar.slug,
            "related_url": instance.event.related_url if instance.event.related_url else None,
            "related_page": instance.event.related_page.slug if instance.event.related_page else None,
        }

        if occurrence:
            result = {
                **result,
                **{
                    "occurrence_id": occurrence.id,
                    "start": occurrence.start,
                    "end": occurrence.end,
                    "cancelled": occurrence.cancelled,
                },
            }

        return {
            **result,
            **extra,
        }
