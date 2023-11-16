from django.urls import path
from app_routes.views import *

urlpatterns = [
    path('', flight_list, name='index'),
]