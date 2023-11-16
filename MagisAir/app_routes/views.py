from django.http import HttpResponse
from django.shortcuts import render
from .models import BaseFlight
from django.views import View 

# Create your views here.

def flight_list(request):
    flights = BaseFlight.objects.all()
    return render(request, 'app_routes/routes.html', {'flights': flights})
