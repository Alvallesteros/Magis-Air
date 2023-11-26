from django.urls import path
from app_crew.views import *

urlpatterns = [
    path('', CrewAssignments.as_view(), name='crew_assignments'),
    path('<str:filter_type>', CrewAssignments.as_view(), name='crew_assignments_filtered')
]