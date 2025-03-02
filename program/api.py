from django.urls import path

from program.views import CalendarView, EventsView, EventView, TagsView

urlpatterns = [
    path("program/events/", EventsView.as_view()),
    path("program/events/<int:pk>/", EventView.as_view()),
    path("program/categories/", TagsView.as_view()),
    path("program/calendars/<slug>", CalendarView.as_view()),
]
