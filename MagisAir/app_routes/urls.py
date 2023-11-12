from django.urls import path
from app_routes.views import *

urlpatterns = [
    path('', index, name='index'),
]