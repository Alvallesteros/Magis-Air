from django.contrib import admin
from .models import Route, BaseFlight

# Register your models here.

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_id', 'origin', 'destination']
    search_fields = ['origin', 'destination']

@admin.register(BaseFlight)
class BaseFlightAdmin(admin.ModelAdmin):
    list_display = ['flight_code', 'flight_type', 'route']
    search_fields = ['flight_code', 'flight_type']
