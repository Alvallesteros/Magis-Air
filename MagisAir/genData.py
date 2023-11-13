import os
import django
import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Set the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MagisAir.settings')
django.setup()

from app_routes.models import Route, BaseFlight
from app_schedule.models import ScheduledFlight
from app_crew.models import CrewMember, CrewAssignment
from app_booking.models import Passenger, Item, Booking, Ticket, BookingItem

# Generate sample data using Faker
fake = Faker()

def generate_routes(num_routes):
    for _ in range(num_routes):
        route = Route(
            origin=fake.city(),
            destination=fake.city(),
        )
        route.save()

def generate_base_flights(num_base_flights):
    route_ids = list(Route.objects.values_list('route_id', flat=True))
    for _ in range(num_base_flights):
        base_flight = BaseFlight(
            flight_type=random.choice(['Connecting', 'Direct', 'Non-Stop']),
            route_id=random.choice(route_ids),
        )
        base_flight.save()

def generate_scheduled_flights(num_scheduled_flights):
    base_flight_ids = list(BaseFlight.objects.values_list('id', flat=True))
    for _ in range(num_scheduled_flights):
        scheduled_flight = ScheduledFlight(
            departure_date=fake.date_between(start_date='+10d', end_date='+90d'),
            departure_time=datetime.strptime(fake.time(), '%H:%M:%S').time(),
            duration=f"{random.randint(1, 5)}:{random.randint(0, 59)}",
            flight_cost=random.uniform(1000, 10000),
            base_flight_id=random.choice(base_flight_ids),
        )
        scheduled_flight.save()

def generate_crew_member(num_crew_member):
    for _ in range(num_crew_member):
        crew_member = CrewMember(
            last_name = fake.last_name(),
            first_name = fake.first_name(),
            middle_initial = fake.random_uppercase_letter()
        )
        crew_member.save()

def generate_crew_assignment(num_crew_assignment):
    crew_member_ids = list(CrewMember.objects.values_list('crew_member_id', flat=True))
    scheduled_flight_ids = list(ScheduledFlight.objects.values_list('scheduled_flight_id', flat=True))
    for _ in range(num_crew_assignment):
        crew_assignment = CrewAssignment(
            scheduled_flight_id_id = random.choice(scheduled_flight_ids), #TODO REMOVE _id
            crew_member_id_id = random.choice(crew_member_ids), #TODO REMOVE _id
            role = random.choice(['Pilot', 'First Officer', 'Flight Attendant', 'Other'])
        )
        crew_assignment.save()

def generate_passenger(num_passenger):
    for _ in range(num_passenger):
        passenger = Passenger(
            last_name = fake.last_name(),
            first_name = fake.first_name(),
            middle_initial = fake.random_uppercase_letter(),
            birthday = fake.date_of_birth(),
            gender = random.choice(['M', 'F', 'O'])
        )
        passenger.save()

def generate_item(num_item):
    for _ in range(num_item):
        item = Item(
            item_name = random.choice(["Terminal Fees", "Travel Insurance", f"Additional Baggage Charge ({random.randint(1,10)} kg)"]),
            description = fake.sentence(),
            item_cost = random.uniform(50, 500)
        )
        item.save()

def generate_booking(num_booking):
    passengers_id = list(Passenger.objects.values_list('passenger_id', flat=True))
    for _ in range(num_booking):
        booking = Booking(
            passenger_id_id = random.choice(passengers_id), #TODO REMOVE _id
            booking_date=fake.date_between(start_date='-90d', end_date='-10d'),
            booking_time=datetime.strptime(fake.time(), '%H:%M:%S').time(),
        )
        booking.save()

def generate_ticket(num_ticket):
    booking_ids = list(Booking.objects.values_list('booking_id', flat=True))
    schedule_flight_ids = list(ScheduledFlight.objects.values_list('scheduled_flight_id', flat=True))
    for _ in range(num_ticket):
        ticket = Ticket(
            booking_id_id = random.choice(booking_ids), #TODO REMOVE _id
            scheduled_flight_id_id = random.choice(schedule_flight_ids), #TODO REMOVE _id
            seat_class = random.choice(['1st Class', 'Business Class', 'Premium Economy Class', 'Regular Economy']), #TODO "CLASS"
            seat_number = f"{fake.random_uppercase_letter()}{random.randint(0,9)}{random.randint(0,9)}"
        )
        ticket.save()

def generate_booking_item(num_bookingitem):
    booking_ids = list(Booking.objects.values_list('booking_id', flat=True))
    item_ids = list(Item.objects.values_list('item_id', flat=True))
    for _ in range(num_bookingitem):
        booking_item = BookingItem(
            booking_id_id = random.choice(booking_ids), #TODO REMOVE _id
            item_id_id = random.choice(item_ids), #TODO REMOVE _id
            item_quantity = random.randint(1,8)
        )
        booking_item.save()

if __name__ == "__main__":
    #Adjust as you want
    num_routes = 10
    num_base_flights = 20
    num_scheduled_flights = 30
    num_crew_member = 40
    num_crew_assignment = 50
    num_passenger = 60
    num_item = 70
    num_booking = 100
    num_ticket = 150
    num_bookingitem = 200

    #Uncomment the following and run the script to generate data

    """    
    generate_routes(num_routes)
    generate_base_flights(num_base_flights)
    generate_scheduled_flights(num_scheduled_flights)
    generate_crew_member(num_crew_member)
    generate_crew_assignment(num_crew_assignment)
    generate_passenger(num_passenger)
    generate_item(num_item)
    generate_booking(num_booking)
    generate_ticket(num_ticket)
    generate_booking_item(num_bookingitem)
    """
