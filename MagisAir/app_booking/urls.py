from django.urls import path
from app_booking.views import *

urlpatterns = [
    path('', BookingView.as_view(), name='booking'),
]