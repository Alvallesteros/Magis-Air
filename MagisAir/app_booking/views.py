from datetime import *

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from django.views import View
from django.db import connection
from .forms import NameSearchForm, DateRangeForm, IdSearchForm

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
        formId = IdSearchForm(request.GET)
        
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

        if formId.is_valid():
            passenger_id = formId.cleaned_data['passenger_id']
            return HttpResponseRedirect(reverse('travel_history', kwargs={'passenger_id': passenger_id}))

        context = {
            "booking_list": booking_list,
            "message": message,
            "form": form,
            "formID": formId
        }

        return render(request, self.template_name, context)

class BookingReportView(View):
    template_name = "app_booking/booking_report.html"

    def get(self, request, filter_type=None, *args, **kwargs):
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

        sum_flight_query = '''
                SELECT bf.flight_code, SUM(t.ticket_cost) AS "ticket_cost"
                FROM app_booking_Ticket t
                JOIN app_booking_Booking b ON t.booking_id = b.booking_id
                JOIN app_schedule_ScheduledFlight sf ON t.scheduled_flight_id = sf.scheduled_flight_id
                JOIN app_routes_BaseFlight bf ON sf.base_flight_id = bf.id
                JOIN app_routes_Route r ON bf.route_id = r.route_id
                {_where}
                GROUP BY bf.flight_code
            '''

        total_query = '''
            SELECT SUM(t.ticket_cost) AS "ticket_cost"
            FROM app_booking_Ticket t
            JOIN app_booking_Booking b ON t.booking_id = b.booking_id
            {_where}
        '''

        if filter_type:
            temp_where, params = self.get_filtered_reports(filter_type)
        elif start_date and end_date:
            temp_where = "WHERE b.booking_date BETWEEN %s AND %s"
            params = [start_date, end_date]
        else:
            temp_where = ''
            params = []

        with connection.cursor() as cursor:
                cursor.execute(sum_flight_query.format(_where=temp_where), params)
                flights_columns = [col[0] for col in cursor.description]
                sum_flights = [dict(zip(flights_columns,row)) for row in cursor.fetchall()]

                cursor.execute(total_query.format(_where=temp_where), params)
                sum_total = cursor.fetchall()[0][0]

        context = {
            "flights": sum_flights,
            "flights_column": formatColumns(flights_columns),
            "total": sum_total,
            "form": form,
        }

        return render(request, self.template_name, context)
    
    def get_filtered_reports(self, filter_type):
        today = date.today()
        if filter_type == "Past Day":
            yesterday = today - timedelta(days=1)
            params = [yesterday, today]
        if filter_type == "Past Week":
            week = today - timedelta(days=7)
            params = [week, today]
        if filter_type == "Past Month":
            month = today - timedelta(days=30)
            params = [month, today]
        if filter_type == "Past Year":
            year = today - timedelta(days=365)
            params = [year, today]

        where = "WHERE b.booking_date BETWEEN %s AND %s"
        return where, params

class TravelHistoryView(View):
    template_name = "app_booking/travel_history.html"

    def get(self, request, passenger_id, *args, **kwargs):
        history_query = '''
            SELECT p.last_name, p.first_name, p.middle_initial, b.booking_id, bf.flight_code, r.origin, r.destination, sf.departure_date
            FROM app_booking_Passenger p
            JOIN app_booking_Booking b ON p.passenger_id = b.passenger_id
            JOIN app_booking_Ticket t ON b.booking_id = t.booking_id
            JOIN app_schedule_ScheduledFlight sf ON t.scheduled_flight_id = sf.scheduled_flight_id
            JOIN app_routes_BaseFlight bf ON sf.base_flight_id = bf.id
            JOIN app_routes_Route r ON bf.route_id = r.route_id
            WHERE p.passenger_id = %s
            ORDER BY sf.departure_date
        '''

        with connection.cursor() as cursor:
                cursor.execute(history_query, [passenger_id])
                columns = [col[0] for col in cursor.description]
                history = [dict(zip(columns, row)) for row in cursor.fetchall()]

        context = {
            "history": history,
        }

        return render(request, self.template_name, context)