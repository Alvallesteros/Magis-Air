from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views import View
from .models import ScheduledFlight

# Create your views here.
class ScheduledFlights(View):
    template_name = 'app_schedule/schedule.html'

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute( '''
                    SELECT bf.flight_code, r.origin, r.destination, sf.departure_time, sf.arrival_time, sf.duration
                    FROM app_schedule_ScheduledFlight AS sf
                    JOIN app_routes_BaseFlight AS bf ON sf.base_flight_id=bf.id
                    JOIN app_routes_Route AS r ON bf.route_id=r.route_id
                ''' )
            results = cursor.fetchall()

        context = {'flights': results}
        return render(request, self.template_name, context)
