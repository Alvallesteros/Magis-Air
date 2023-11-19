from datetime import *

from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.db import connection
from .forms import NameSearchForm

# Create your views here.
class BookingView(View):
    template_name = "app_booking/booking.html"

    def get(self, request, booking_id, *args, **kwargs):

        core_query = '''
            SELECT b.booking_id, b.booking_date, b.booking_time, b.total_cost
            FROM app_booking_Booking b
            WHERE b.booking_id = %s 
        '''
        passenger_query = '''
            SELECT p.last_name, p.first_name, p.middle_initial, p.gender, p.birthday
            FROM app_booking_Passenger p
            JOIN app_booking_Booking b ON p.passenger_id = b.passenger_id
            WHERE b.booking_id = %s
        '''
        item_query = '''
            SELECT (i.item_name || ' ('|| i.description ||')') AS description, bi.item_quantity AS quantity, bi.booking_item_cost AS cost
            FROM app_booking_BookingItem bi
            JOIN app_booking_Item i ON bi.item_id = i.item_id
            WHERE bi.booking_id = %s
        '''
        flight_query = '''
            SELECT bf.flight_code, r.origin, r.destination, (sf.departure_date || ', ' || sf.departure_time) AS departure, (sf.arrival_date || ', ' || sf.arrival_time) AS arrival, sf.duration, t.ticket_cost
            FROM app_booking_ticket t
            JOIN app_schedule_ScheduledFlight sf ON t.scheduled_flight_id = sf.scheduled_flight_id
            JOIN app_routes_BaseFlight bf ON sf.base_flight_id = bf.id
            JOIN app_routes_Route r ON bf.route_id = r.route_id
            WHERE t.booking_id = %s
            ORDER BY sf.departure_date
        '''

        context = {
            "booking": getBookingQuery(booking_id, core_query),
            "passenger": getBookingQuery(booking_id, passenger_query),
            "item": getBookingQuery(booking_id, item_query),
            "flight": getBookingQuery(booking_id, flight_query),
        }

        return render(request, self.template_name, context)

def formatColumns(lst):
    temp_lst = lst
    lst = [col.replace('_', ' ').title() for col in temp_lst]
    return lst

def getBookingQuery(booking_id, query):
    with connection.cursor() as cursor:
            cursor.execute(query, [booking_id])
            columns = [col[0] for col in cursor.description]
            content = [dict(zip(columns, row)) for row in cursor.fetchall()]

    ##FORMATTING##
    for items in content:
        if 'gender' in items:
            items['gender'] = f"{"Male" if content[0]['gender'] == 'M' else ("Female" if content[0]['gender'] == 'F' else "Other")}"
        if 'departure' in items:
            temp = datetime.strptime(items['departure'], "%Y-%m-%d, %H:%M:%S")
            items['departure'] = temp.strftime("%d %b %Y, %H:%M")
        if 'arrival' in items:
            temp = datetime.strptime(items['arrival'], "%Y-%m-%d, %H:%M:%S")
            items['arrival'] = temp.strftime("%d %b %Y, %H:%M")
        if 'duration' in items:
            hours, minutes = map(int, items['duration'].split(':'))
            items['duration'] = f"{hours} {'hour' if hours == 1 else 'hours'} {minutes} {'minute' if minutes == 1 else 'minutes'}"

    return {"content": content, "columns": formatColumns(columns)}

class BookingListView(View):
    template_name = "app_booking/booking_list.html"

    def get(self, request, *args, **kwargs):
        form = NameSearchForm(request.GET)
        
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            message = 'You have the following bookings:'

            name_query = '''
                SELECT b.booking_id
                FROM app_booking_Passenger p
                JOIN app_booking_Booking b ON p.passenger_id = b.passenger_id
                WHERE UPPER(p.first_name) LIKE UPPER(%s)
                    AND UPPER(p.last_name) LIKE UPPER(%s)
            '''

            with connection.cursor() as cursor:
                cursor.execute(name_query, [first_name, last_name])
                columns = [col[0] for col in cursor.description]
                booking_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            message = 'Please enter your name'
            booking_list = []

        context = {
            "booking_list": booking_list,
            "message": message,
            "form": form
        }

        return render(request, self.template_name, context)
