from django.urls import re_path
from schedule.views import api_occurrences

urlpatterns = [
    re_path("^program", api_occurrences),
]
