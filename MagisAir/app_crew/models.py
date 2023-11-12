from django.db import models

# Create your models here.

# Crew Member
class CrewMember(models.Model):
    crew_member_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"