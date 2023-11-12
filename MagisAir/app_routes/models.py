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
    flight_code = models.CharField(max_length=6, unique=True, null=False, blank=True)
    flight_type_choices = [
        ('Connecting', 'Connecting'),
        ('Direct', 'Direct'),
        ('Non-Stop', 'Non-Stop'),
    ]
    flight_type = models.CharField(max_length=20, choices=flight_type_choices, null=False)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.flight_code:
            max_flight_code = BaseFlight.objects.all().order_by('flight_code').last()
            max_flight_num = int(max_flight_code.flight_code[2:]) if max_flight_code else 0
            self.flight_code = f"MA{max_flight_num + 1:04d}"
        super(BaseFlight, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight_type} Flight {self.flight_code}: {self.route.origin} to {self.route.destination}"