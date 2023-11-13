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
from app_crew.models import CrewMember

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


if __name__ == "__main__":
    num_routes = 10
    num_base_flights = 20
    num_scheduled_flights = 30
    num_crew_member = 40

    #generate_routes(num_routes)
    #generate_base_flights(num_base_flights)
    #generate_scheduled_flights(num_scheduled_flights)
    #generate_crew_member(num_crew_member)
