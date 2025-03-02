from rest_framework.serializers import ModelSerializer
from schedule.models import Calendar
from taggit.serializers import TaggitSerializer

from program.models import Event, EventTag, Tag


class EventTagSerializer(ModelSerializer):
    class Meta:
        model = EventTag
        fields = "__all__"

    def to_representation(self, instance):
        return [
            {
                "id": tag.id,
                "name": tag.name,
            }
            for tag in instance.all()
        ]


class CalendarSerializer(ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"


class EventSerializer(TaggitSerializer, ModelSerializer):
    cancelled = "cancelled"

    class Meta:
        model = Event
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "tags": EventTagSerializer().to_representation(instance.tags),
            "start": instance.start,
            "end": instance.end,
            # "existed": instance.existed,
            "color": instance.event.color_event,
            "description": instance.description,
            # "rule": recur_rule,
            # "end_recurring_period": recur_period_end,
            # "creator": str(instance.event.creator),
            "calendar": instance.event.calendar.slug,
            # "cancelled": instance.cancelled,
        }
