from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection 
from django.views import View 
from .forms import DateFilterForm
from datetime import *

# Create your views here.
class CrewAssignments(View):
    template_name = 'app_crew/crew.html'

    def get(self, request, filter_type=None, *args, **kwargs):
        form = DateFilterForm(request.GET)
        query = '''
                SELECT 
                    (cm.last_name || ', ' || cm.first_name) AS "crew",
                    ca.role,
                    bf.flight_code AS "flight",
                    fr.destination AS "destination",
                    (sf.departure_date || ', ' || sf.departure_time) AS departure, 
                    (sf.arrival_date || ', ' || sf.arrival_time) AS arrival
                FROM app_crew_CrewMember AS cm
                JOIN app_crew_CrewAssignment AS ca ON cm.crew_member_id = ca.crew_member_id
                JOIN app_schedule_ScheduledFlight AS sf ON ca.scheduled_flight_id = sf.scheduled_flight_id
                JOIN app_routes_BaseFlight AS bf ON sf.base_flight_id=bf.id
                JOIN app_routes_Route AS fr ON bf.route_id=fr.route_id
                {_where}
                ORDER BY bf.flight_code
                '''
        
        with connection.cursor() as cursor:

            if filter_type:
                params, where = self.get_filtered_crew(filter_type)
            elif form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                if start_date and end_date: # check if date is not None
                    params = [start_date, end_date]
                    where = 'WHERE sf.departure_date BETWEEN %s AND %s'
                else:
                    params = []
                    where=''
            else: # if not valid (just failsafe)
                params = []
                where=''
            
            cursor.execute(query.format(_where=where), params)
            columns = [col[0] for col in cursor.description]
            results = [dict (zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.title() for col in columns]

            for r in results: # format departure, arrival datetimes and crew names
                r['departure'] = datetime.strptime(r['departure'], "%Y-%m-%d, %H:%M:%S").strftime("%d %b %Y, %H:%M")
                r['arrival'] = datetime.strptime(r['arrival'], "%Y-%m-%d, %H:%M:%S").strftime("%d %b %Y, %H:%M")            
        
        context = {
            'headers' : formatted_columns,
            'rows' : results,
            'form' : form
        }

        return render(request, self.template_name, context)

    def get_filtered_crew(self, filter_type):
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

        where = "WHERE sf.departure_date BETWEEN %s AND %s"
        return params, where