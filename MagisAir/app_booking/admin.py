from django.contrib import admin
from .models import Passenger, Item

# Register your models here.
@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passenger_id', 'last_name', 'first_name', 'middle_initial', 'birthday', 'gender')
    search_fields = ('last_name', 'first_name')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_name', 'description', 'item_cost')
    search_fields = ('item_name', 'description')