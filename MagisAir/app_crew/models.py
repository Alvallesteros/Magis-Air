from django.db import models
from app_schedule.models import ScheduledFlight

# Create your models here.

# Crew Member
class CrewMember(models.Model):
    crew_member_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CrewAssignment(models.Model):
    crew_id = models.AutoField(primary_key=True)
    scheduled_flight_id = models.ForeignKey(ScheduledFlight, on_delete=models.CASCADE)
    crew_member_id = models.ForeignKey(CrewMember, on_delete=models.CASCADE)

    # Attribute: Role
    ROLE_CHOICES = [
        ('Pilot', 'Pilot'),
        ('First Officer', 'First Officer'),
        ('Flight Attendant', 'Flight Attendant'),
        ('Other', 'Other'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)

    def __str__(self):
        return f"Crew Assignment {self.crew_id}: {self.crew_member_id.last_name}, {self.crew_member_id.first_name} - {self.scheduled_flight_id.base_flight.flight_code} - {self.role}"