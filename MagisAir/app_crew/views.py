from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection 
from django.views import View 
from .models import CrewMember, CrewAssignment

# Create your views here.
class CrewAssignments(View):
    template_name = 'app_crew/crew.html'

    def get(self, request, *args, **kwargs):
        query = '''
                SELECT 
                    CONCAT(cm.last_name, ', ', cm.first_name) AS "crew",
                    ca.role,
                    bf.flight_code AS "flight",
                    fr.destination AS "destination",
                    CONCAT(sf.departure_date, ', ', sf.departure_time) AS "departure",
                    CONCAT(sf.arrival_date, ', ', sf.arrival_time) AS "arrival"
                    FROM app_crew_CrewMember AS cm
                    JOIN app_crew_CrewAssignment AS ca ON cm.crew_member_id=ca.crew_member
                    JOIN app_schedule_ScheduledFlight AS sf ON ca.scheduled_flight=sf.scheduled_flight_id
                    JOIN app_routes_BaseFlight AS bf ON sf.base_flight=bf.id
                    JOIN app_routes_Route AS fr ON bf.route=fr.route_id
                    {_where}
                '''
        
        with connection.cursor() as cursor:
            cursor.execute(query.format(_where=''))
            columns = [col[0] for col in cursor.description]
            results = [dict (zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.title() for col in columns]

        context = {
            'headers' : formatted_columns,
            'rows' : results
        }

        return render(request, self.template_name, context)