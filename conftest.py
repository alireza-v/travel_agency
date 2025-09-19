from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

from tickets.models import Flight, FlightTicket, Hotel, HotelReserve, Tour, TourReserve

User = get_user_model()
faker = Faker()


@pytest.fixture
def user(db):
    email = "test@email.com"
    password = "1234QWqw"
    return User.objects.create_user(
        email=email,
        password=password,
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def jwt(db, client, user):
    url = reverse("jwt:jwt-create")
    resp = client.post(
        url,
        data={
            "email": user.email,
            "password": "1234QWqw",
        },
    )
    tokens = resp.json()
    return (tokens["access"], tokens["refresh"])


@pytest.fixture
def tour(db, user):
    """Tour model fixture"""
    return Tour.objects.create(
        user=user,
        image=faker.city() + "jpg",
        description=faker.text(max_nb_chars=20),
        origin="Isfahan",
        destination="Tabriz",
        rest_place=faker.text(),
        departure_time=datetime.today(),
        arrival_time=datetime.today() + timedelta(days=3),
        agency=faker.name(),
        price=faker.pyfloat(left_digits=10, right_digits=3),
    )


@pytest.fixture
def flight(db, user, tour):
    """Flight model fixture"""
    return Flight.objects.create(
        user=user,
        origin="Isfahan",
        destination="Tabriz",
        departure_time=datetime.today(),
        arrival_time=datetime.today() + timedelta(days=3),
        ticket_price="120.00",
        agency="air_agency",
    )


@pytest.fixture
def hotel(db, user):
    """Hotel model fixture"""
    return Hotel.objects.create(
        user=user,
        destination=faker.city(),
        arrival_time=datetime.today(),
        departure_time=datetime.today() + timedelta(days=3),
    )


@pytest.fixture
def tour_reservation(db, tour, user):
    """TourReserve model fixture"""

    return TourReserve.objects.create(
        user=user,
        tour=tour,
    )


@pytest.fixture
def flight_ticket(db, user, flight):
    """FlightTicket model fixture"""
    return FlightTicket.objects.create(
        user=user,
        flight=flight,
    )


@pytest.fixture
def hotel_reservation(db, user, hotel):
    """HotelReserve model fixture"""
    return HotelReserve.objects.create(
        user=user,
        hotel=hotel,
    )


@pytest.fixture
def setup_authenticated_client(client, jwt):
    """JWT authentication setup"""

    access, _ = jwt
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.mark.django_db
class BaseTest:
    """Base test class to handle authentication setup."""

    @pytest.fixture(autouse=True)
    def authenticated_client(self, setup_authenticated_client):
        """This fixture be used in all test classes"""
        self.client = setup_authenticated_client

    @pytest.fixture(autouse=True)
    def setup_objects(
        self,
        user,
        tour,
        flight,
        hotel,
        tour_reservation,
        flight_ticket,
        hotel_reservation,
    ):
        self.user = user
        self.tour = tour
        self.flight = flight
        self.hotel = hotel
        self.tour_reservation = tour_reservation
        self.flight_ticket = flight_ticket
        self.hotel_reservation = hotel_reservation
