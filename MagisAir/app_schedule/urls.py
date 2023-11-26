from django.urls import path
from app_schedule.views import ScheduledFlights

urlpatterns = [
    path('', ScheduledFlights.as_view(), name='schedule-flight'),
]