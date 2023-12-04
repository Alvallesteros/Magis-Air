from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import BaseFlight, Route
from .forms import RouteForm

# Create your views here.


def flight_list(request):
    flights = BaseFlight.objects.all()
    return render(request, 'app_routes/routes.html', {'flights': flights})


def create_route(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            new_route = Route(
                origin=form.cleaned_data.get('origin_name'),
                destination=form.cleaned_data.get('destination_name'),
            )
            new_route.save()
            return redirect('index')

    else:
        form = RouteForm()

    return render(request, 'app_routes/create_route.html', {'form': form})

class CreateBaseFlightView(CreateView):
    model = BaseFlight
    template_name = 'app_routes/create_base_flight.html'
    fields = ["flight_type", "route"]

    def get_success_url(self):
        return reverse('index')
