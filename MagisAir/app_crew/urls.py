from django.urls import path
from app_crew.views import *

urlpatterns = [
    path('', CrewAssignments.as_view(), name='index'),
]