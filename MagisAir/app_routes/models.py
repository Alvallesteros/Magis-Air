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
    flight_code = models.CharField(max_length=6, unique=True, null=False) #Manually Create a new Flight ID
    flight_type_choices = [
        ('Connecting', 'Connecting'),
        ('Direct', 'Direct'),
        ('Non-Stop', 'Non-Stop'),
    ]
    flight_type = models.CharField(max_length=20, choices=flight_type_choices, null=False)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.flight_type_choices} Flight {self.flight_code}: {self.route.origin} to {self.route.destination}"