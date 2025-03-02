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
    list_display = ("title", "start", "end", "calendar")
    search_fields = ("title", "description")

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
