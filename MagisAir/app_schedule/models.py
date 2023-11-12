from datetime import datetime, timedelta

from django.db import models
from app_routes.models import BaseFlight

# Create your models here.

class ScheduledFlight(models.Model):
    # Scheduled_Flight_ID
    scheduled_flight_id = models.AutoField(primary_key=True)
    departure_date = models.DateField(null=False)
    departure_time = models.TimeField(null=False)
    arrival_date = models.DateField(null=False, blank=True)
    arrival_time = models.TimeField(null=False, blank=True)
    duration = models.CharField(max_length=10)
    flight_cost = models.FloatField(null=False)
    base_flight = models.ForeignKey(BaseFlight, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calculate Arrival_Date and Arrival_Time based on Departure_Date, Departure_Time, and Duration
        if self.departure_date and self.departure_time and self.duration:
            departure_datetime = datetime.combine(self.departure_date, self.departure_time) # Convert Departure_Date and Departure_Time to datetime

            hours, minutes = map(int, self.duration.split(':')) # Parse Duration to extract hours and minutes

            total_minutes = hours * 60 + minutes # Calculate the total duration in minutes

            # Calculate Arrival_Date and Arrival_Time
            arrival_datetime = departure_datetime + timedelta(minutes=total_minutes)
            self.arrival_date = arrival_datetime.date()
            self.arrival_time = arrival_datetime.time()

        super(ScheduledFlight, self).save(*args, **kwargs)

    def __str__(self):
        return f"Scheduled Flight {self.scheduled_flight_id}: Flight {self.base_flight.flight_code} Departing at {self.departure_date}, {self.departure_time}"
