from django.contrib import admin
from .models import ScheduledFlight
# Register your models here.

@admin.register(ScheduledFlight)
class ScheduledFlightAdmin(admin.ModelAdmin):
    list_display = ('scheduled_flight_id', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'duration', 'flight_cost', 'base_flight')
    list_filter = ('departure_date', 'arrival_date', 'base_flight')
    search_fields = ('scheduled_flight_id', 'base_flight')
