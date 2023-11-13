from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views import View
from .models import ScheduledFlight

# Create your views here.
class ScheduledFlights(View):
    template_name = 'app_schedule/schedule.html'

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:                 #SOURCE: https://docs.djangoproject.com/en/4.2/topics/db/sql/
            cursor.execute( '''
                    SELECT bf.flight_code, r.origin, r.destination, sf.departure_time AS "departure", sf.arrival_time AS "arrival", sf.duration
                    FROM app_schedule_ScheduledFlight AS sf
                    JOIN app_routes_BaseFlight AS bf ON sf.base_flight_id=bf.id
                    JOIN app_routes_Route AS r ON bf.route_id=r.route_id
                ''' )
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.replace('_', ' ').title() for col in columns]

            for r in results:
                r['duration'] = self.format_duration(r['duration'])

        context = { 'flights': results,
                    'column_names': formatted_columns 
                    }
        return render(request, self.template_name, context)

    def format_duration(self, duration):
            hours, minutes = map(int, duration.split(':'))
            formatted_duration = f"{hours} {'hour' if hours == 1 else 'hours'} {minutes} {'minute' if minutes == 1 else 'minutes'}"
            return formatted_duration