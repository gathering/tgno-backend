from rest_framework import generics
from schedule.models import Calendar
from taggit.serializers import TaggitSerializer

from program.models import Event, Tag
from program.serializers import CalendarSerializer, EventSerializer, EventTagSerializer

# Duplicated key views from `schedule` package in order to support
# regular Django Rest Framework behaviour, and additional filtering criteria


class TagsView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = EventTagSerializer


class CalendarView(generics.RetrieveAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = "slug"


class EventView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# Our new entrypoint, replaces `schedule.views.api_occurrences`
class EventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
