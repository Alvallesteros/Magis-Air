from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection 
from django.views import View 
from .models import CrewMember, CrewAssignment
import datetime as dt
from .forms import DateFilterForm

# Create your views here.
class CrewAssignments(View):
    template_name = 'app_crew/crew.html'

    def dateTimeTransform(self, date, time):
            return date.strftime('%-d %B %Y') + ', ' + time.strftime('%H:%M')
        
    def nameTransform(self, first, last):
        return last + ', ' + first

    def get(self, request, *args, **kwargs):
        form = DateFilterForm(request.GET)
        query = '''
                SELECT 
                    cm.last_name,
                    sf.arrival_time,
                    sf.departure_time,
                    cm.first_name AS "crew",
                    ca.role,
                    bf.flight_code AS "flight",
                    fr.destination AS "destination",
                    sf.departure_date AS "departure",
                    sf.arrival_date AS "arrival"
                    FROM app_crew_CrewMember AS cm
                    JOIN app_crew_CrewAssignment AS ca ON cm.crew_member_id = ca.crew_member_id
                    JOIN app_schedule_ScheduledFlight AS sf ON ca.scheduled_flight_id = sf.scheduled_flight_id
                    JOIN app_routes_BaseFlight AS bf ON sf.base_flight_id=bf.id
                    JOIN app_routes_Route AS fr ON bf.route_id=fr.route_id
                    {_where}
                    ORDER BY bf.flight_code
                '''
        
        with connection.cursor() as cursor:
            if form.is_valid():
                filter_date = form.cleaned_data['filter_date']                 
                cursor.execute(query.format(_where='WHERE sf.departure_date = %s'), [filter_date])
            else:
                cursor.execute(query.format(_where=''))

            columns = [col[0] for col in cursor.description]
            results = [dict (zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.title() for col in columns][3:]

            for r in results:
                r['departure'] = self.dateTimeTransform(r['departure'], r['departure_time'])
                r['arrival'] = self.dateTimeTransform(r['arrival'], r['arrival_time'])
                r['crew'] = self.nameTransform(r['crew'], r['last_name'])

        context = {
            'headers' : formatted_columns,
            'rows' : results,
            'form' : form
        }

        return render(request, self.template_name, context)