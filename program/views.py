import datetime

import pytz
from django.conf import settings
from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework import generics
from schedule.models import Calendar, Occurrence

from program.models import Event, Tag
from program.serializers import CalendarSerializer, EventSerializer, EventTagSerializer

# Duplicated key views from `schedule` package in order to support
# regular Django Rest Framework behaviour, and additional filtering criteria


class TagsView(generics.ListAPIView):
    queryset = Tag.objects.all().filter(hidden=False)
    serializer_class = EventTagSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type = self.request.GET.get("type")
        if type:
            queryset = queryset.filter(type=type)
        return queryset


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

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        start = self.request.GET.get("start", "{year}-01-01".format(year=now.year))
        end = self.request.GET.get("end", "{year}-01-01".format(year=now.year + 1))
        timezone = self.request.GET.get("timezone")
        tags = self.request.GET.get("tags")
        calendar_slug = self.request.GET.get("calendar_slug")

        queryset = self.get_queryset()

        if calendar_slug:
            queryset = queryset.filter(calendar__slug=calendar_slug)

        queryset = queryset.filter(start__lte=end).filter(
            Q(end_recurring_period__gte=start) | Q(end_recurring_period__isnull=True)
        )

        if tags:
            queryset = queryset.filter(tags__slug__in=tags.split(","))

        events = api_occurrences(queryset, start, end, timezone)

        return JsonResponse(events, safe=False)


# Replaces `schedule.views.api_occurrences` to make extensions possible
# Main changes:
# - Passing in queryset (removes some initial filtering and lookup logic
# - Using custom serializers that takes both Event and Occurrence into account
def api_occurrences(queryset, start, end, timezone):
    if not start or not end:
        raise ValueError("Start and end parameters are required")
    # version 2 of full calendar
    # TODO: improve this code with date util package
    if "-" in start:

        def convert(ddatetime):
            if ddatetime:
                ddatetime = ddatetime.split(" ")[0]
                try:
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%d")
                except ValueError:
                    # try a different date string format first before failing
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%dT%H:%M:%S")

    else:

        def convert(ddatetime):
            return datetime.datetime.utcfromtimestamp(float(ddatetime))

    start = convert(start)
    end = convert(end)
    current_tz = False
    if timezone and timezone in pytz.common_timezones:
        # make start and end dates aware in given timezone
        current_tz = pytz.timezone(timezone)
        start = current_tz.localize(start)
        end = current_tz.localize(end)
    elif settings.USE_TZ:
        # If USE_TZ is True, make start and end dates aware in UTC timezone
        utc = pytz.UTC
        start = utc.localize(start)
        end = utc.localize(end)

    response_data = []
    # Algorithm to get an id for the occurrences in fullcalendar (NOT THE SAME
    # AS IN THE DB) which are always unique.
    # Fullcalendar thinks that all their "events" with the same "event.id" in
    # their system are the same object, because it's not really built around
    # the idea of events (generators)
    # and occurrences (their events).
    # Check the "persisted" boolean value that tells it whether to change the
    # event, using the "event_id" or the occurrence with the specified "id".
    # for more info https://github.com/llazzaro/django-scheduler/pull/169
    i = 1
    if Occurrence.objects.all().exists():
        i = Occurrence.objects.latest("id").id + 1

    for event in queryset:
        occurrences = event.get_occurrences(start, end)
        for occurrence in occurrences:
            occurrence_id = i + occurrence.event.id
            existed = False

            if occurrence.id:
                occurrence_id = occurrence.id
                existed = True

            recur_rule = occurrence.event.rule.name if occurrence.event.rule else None

            if occurrence.event.end_recurring_period:
                recur_period_end = occurrence.event.end_recurring_period
                if current_tz:
                    # make recur_period_end aware in given timezone
                    recur_period_end = recur_period_end.astimezone(current_tz)
                recur_period_end = recur_period_end
            else:
                recur_period_end = None

            event_start = occurrence.start
            event_end = occurrence.end
            if current_tz:
                # make event start and end dates aware in given timezone
                event_start = event_start.astimezone(current_tz)
                event_end = event_end.astimezone(current_tz)
            if occurrence.cancelled:
                # fixes bug 508
                continue

            response_data.append(
                EventSerializer().to_representation(
                    event,
                    occurrence,
                    {
                        "occurrence_id": occurrence_id,
                        "existed": existed,
                        "rule": recur_rule,
                        "end_recurring_period": recur_period_end,
                    },
                )
            )

    return response_data
