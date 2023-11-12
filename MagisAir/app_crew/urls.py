from django.urls import path
from app_crew.views import *

urlpatterns = [
    path('', index, name='index'),
]