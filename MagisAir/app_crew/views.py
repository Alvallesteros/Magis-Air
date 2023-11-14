from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection 
from django.views import View 
from .forms import DateFilterForm

# Create your views here.
class CrewAssignments(View):
    template_name = 'app_crew/crew.html'

    def dateTimeTransform(self, date, time): # combine date and time columns into one
            return date.strftime('%-d %B %Y') + ', ' + time.strftime('%H:%M')
        
    def nameTransform(self, first, last): # combine last and firstnames into one
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
                start_date = form.cleaned_data['filter_date']
                if start_date == None: # check if no date (default get) because i set required=False to remove error msg
                    where=''
                else: # this is if date
                    where = 'WHERE sf.departure_date = %s'.format(start_date)
            else: # if not valid (just failsafe)
                where=''
            cursor.execute(query.format(_where=where))
            columns = [col[0] for col in cursor.description]
            results = [dict (zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.title() for col in columns][3:] # first columns are only for formatting name and dates

            for r in results: # format departure, arrival datetimes and crew names
                r['departure'] = self.dateTimeTransform(r['departure'], r['departure_time'])
                r['arrival'] = self.dateTimeTransform(r['arrival'], r['arrival_time'])
                r['crew'] = self.nameTransform(r['crew'], r['last_name'])

        context = {
            'headers' : formatted_columns,
            'rows' : results,
            'form' : form
        }

        return render(request, self.template_name, context)