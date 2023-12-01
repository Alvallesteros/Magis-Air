from django.urls import path
from app_routes.views import *

urlpatterns = [
    path('', flight_list, name='index'),
    path('create_route/', create_route, name='create-route'),
    path('create_base/', CreateBaseFlightView.as_view(), name='create-base-flight')
]
