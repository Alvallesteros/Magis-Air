from django.urls import path
from app_crew.views import *

urlpatterns = [
    path('', CrewAssignments.as_view(), name='crew_assignments'),
    path('<str:filter_type>', CrewAssignments.as_view(), name='crew_assignments_filtered'),
    path('create_crew/', CreateCrewView.as_view(), name='crew-create'),
    path('create_assignment/', CreateAssignmentView.as_view(), name='assignment-create')
]
