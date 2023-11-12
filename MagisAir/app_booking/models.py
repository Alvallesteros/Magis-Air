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

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    passenger_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"Booking {self.booking_id}"


class BookingItem(models.Model):
    booking_item_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_quantity = models.IntegerField(null=False)
    booking_item_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)

    def save(self, *args, **kwargs):
        
        if self.item_quantity and self.item_id:
            self.booking_item_cost = self.item_quantity * self.item_id.item_cost

        super(BookingItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_id} | {self.booking_id}"
