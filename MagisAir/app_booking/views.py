from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.db import connection

# Create your views here.
class BookingView(View):
    template_name = "app_booking/booking.html"

    name = ""

    def get(self, request, *args, **kwargs):
        raw_query = '''
                        SELECT * 
                        FROM app_booking_Booking b
                        JOIN app_booking_Passenger p ON b.passenger_id = p.passenger_id
                        WHERE UPPER(p.first_name) LIKE "TAYLOR"
                            AND UPPER(p.last_name) LIKE "ODOM"
                            AND b.booking_id = 40;
                    '''

        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            columns = [col[0] for col in cursor.description]
            booking = [dict(zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.replace('_', ' ').title() for col in columns]

        context = {
            "booking_content": booking,
            "column_names": formatted_columns
        }

        return render(request, self.template_name, context)
