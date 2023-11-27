from django.contrib import admin
from .models import Passenger, Item, Booking, BookingItem, Ticket

# Register your models here.
@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passenger_id', 'last_name', 'first_name', 'middle_initial', 'birthday', 'gender')
    search_fields = ('last_name', 'first_name')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'description', 'item_cost')
    search_fields =['description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'passenger_id', 'booking_date', 'booking_time', 'total_cost')
    search_fields = ('booking_id', 'passenger_id', 'total_cost')
    readonly_fields = ('total_cost', 'booking_date', 'booking_time')

@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ('booking_item_id', 'booking_id', 'item_id', 'item_quantity', 'booking_item_cost')
    list_filter = ('booking_id', 'item_id')
    search_fields = ('booking_id__booking_id', 'item_id__item_name') 
    readonly_fields = ('booking_item_cost',) 

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'booking_id', 'scheduled_flight_id', 'seat_class', 'seat_number', 'ticket_cost')
    list_filter = ('booking_id', 'scheduled_flight_id')
    search_fields = ('booking_id__booking_id', 'scheduled_flight_id__scheduled_flight_id')
    readonly_fields = ('ticket_cost',)
