from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views import View
from .models import ScheduledFlight
from .forms import DateFilterForm

# Create your views here.
class ScheduledFlights(View):
    template_name = 'app_schedule/schedule.html'

    def get(self, request, *args, **kwargs):
        form = DateFilterForm(request.GET)
        raw_query='''
            SELECT bf.flight_code, r.origin, r.destination, sf.departure_time AS "departure", sf.arrival_time AS "arrival", sf.duration
                    FROM app_schedule_ScheduledFlight AS sf
                    JOIN app_routes_BaseFlight AS bf ON sf.base_flight_id=bf.id
                    JOIN app_routes_Route AS r ON bf.route_id=r.route_id
                    {_where}
                    '''

        with connection.cursor() as cursor:                             #SOURCE: https://docs.djangoproject.com/en/4.2/topics/db/sql/
            if form.is_valid():
                filter_date = form.cleaned_data['filter_date']                 
                cursor.execute(raw_query.format(_where='WHERE sf.departure_date = %s'), [filter_date])
            else:
                cursor.execute(raw_query.format(_where=''))

            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            formatted_columns = [col.replace('_', ' ').title() for col in columns]

            for r in results:
                r['duration'] = self.format_duration(r['duration'])

        context = { 'flights': results,
                    'column_names': formatted_columns,
                    'form': form,
                    'date': filter_date
                    }

        return render(request, self.template_name, context)

    def format_duration(self, duration):
            hours, minutes = map(int, duration.split(':'))
            formatted_duration = f"{hours} {'hour' if hours == 1 else 'hours'} {minutes} {'minute' if minutes == 1 else 'minutes'}"
            return formatted_duration