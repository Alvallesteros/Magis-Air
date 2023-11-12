from django.db import models

# Create your models here.
class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    middle_initial = models.CharField(max_length=1, null=True, blank=True)
    birthday = models.DateField(null=False)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.item_id}: {self.item_name}"
