from django.urls import path
from app_booking.views import *

urlpatterns = [
    path('<int:booking_id>', BookingView.as_view(), name='booking_detail'),
    path('', BookingListView.as_view(), name='booking_list'),
    path('reports/', BookingReportView.as_view(), name='booking_report'),
    path('reports/<str:filter_type>', BookingReportView.as_view(), name='booking_report_filtered'),
    path('history/<int:passenger_id>', TravelHistoryView.as_view(), name='travel_history')
]