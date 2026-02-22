from urllib.parse import urlencode

from schedule.models import Calendar
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from program.models import Event, Tag


class EventTagAdmin(SnippetViewSet):
    model = Tag

    menu_label = "Tags"
    menu_icon = "tag"


class EventModelAdmin(SnippetViewSet):
    model = Event

    menu_label = "Events"
    menu_icon = "date"

    chooser_per_page = 50
    list_per_page = 50
    list_display = ("title", "start", "end", "calendar", "hidden")
    list_filter = ("calendar", "hidden")
    search_fields = ("title", "description")

    def _get_newest_calendar_pk(self):
        cals = Calendar.objects.order_by(*["-pk"]).only("pk")
        # Pick the first calendar that has events (if debugging, changes to this lookup might not happen immediately)
        for cal in cals:
            if Event.objects.filter(calendar=cal).exists():
                event_count = Event.objects.filter(calendar=cal).count()
                print(f"Found calendar with events: {cal.pk}, event count: {event_count}")
                return cal.pk
        return None

    def get_menu_item(self, order=None):
        item = super().get_menu_item(order=order)

        newest_pk = self._get_newest_calendar_pk()
        if newest_pk:
            # item.url is the standard listing URL; add the filter querystring.
            sep = "&" if "?" in item.url else "?"
            item.url = f"{item.url}{sep}{urlencode({'calendar': newest_pk})}"

        return item

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    FieldPanel("title"),
                    FieldPanel("calendar"),
                    FieldPanel("tags", heading="Categories"),
                    FieldPanel("start"),
                    FieldPanel("end"),
                    FieldPanel("description"),
                ],
                heading="Event",
            ),
            ObjectList(
                [
                    FieldPanel("hidden"),
                    FieldPanel("related_url"),
                ],
                heading="Advanced",
            ),
            ObjectList(
                [
                    FieldPanel("related_page"),
                    FieldPanel("rule"),
                    FieldPanel("end_recurring_period"),
                    FieldPanel("color_event"),
                    FieldPanel("creator"),
                ],
                heading="Experimental",
            ),
        ]
    )


class CalendarModelAdmin(SnippetViewSet):
    model = Calendar

    menu_label = "Calendars"
    menu_icon = "dots-horizontal"

    list_display = ("name",)
    search_fields = ("name",)


@register_snippet
class ProgramModelAdmin(SnippetViewSetGroup):
    items = (EventModelAdmin, EventTagAdmin, CalendarModelAdmin)

    menu_label = "Calendar"
    menu_name = "calendar"
    menu_icon = "date"
    add_to_admin_menu = True
