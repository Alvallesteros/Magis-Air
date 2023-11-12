import re
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

#Route Entity
class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=255, null=False, blank=False)
    destination = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"Route {self.route_id}: {self.origin} to {self.destination}"

#BaseFlight Entity
class BaseFlight(models.Model):
    flight_code = models.CharField(max_length=6, unique=True, null=False, help_text='Must be a MA and Four Digits (e.g. MA0001, MA2031, MA9099)') #Manually Create a new Flight ID
    flight_type_choices = [
        ('Connecting', 'Connecting'),
        ('Direct', 'Direct'),
        ('Non-Stop', 'Non-Stop'),
    ]
    flight_type = models.CharField(max_length=20, choices=flight_type_choices, null=False)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def clean(self):
        if not re.match(r'^MA\d{4}$', self.flight_code):
            raise ValidationError('Flight Code Invalid; Must be a MA + Four Digits')

    def __str__(self):
        return f"{self.flight_type} Flight {self.flight_code}: {self.route.origin} to {self.route.destination}"