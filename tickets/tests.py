import jdatetime
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.
from users.tests import *

from .models import *


@pytest.fixture
def jwt(db, client, user):
    """Retrive access/refresh token by validating email and password"""
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


# @pytest.fixture
# def hotel(db, user):
#     """Create Hotel instance for testing"""
#     return Hotel.objects.create(
#         user=user,
#         enter=faker.date_time(),
#         exit=faker.date_time(),
#     )


@pytest.fixture
def tour(db, user):
    """Create Tour instance for testing"""
    return Tour.objects.create(
        user=user,
        image=faker.city() + "jpg",
        info=faker.text(max_nb_chars=20),
        origin=faker.random_int(min=1, max=4),
        destination=faker.random_int(min=1, max=4),
        rest_place=faker.text(),
        start_date=jdatetime.datetime.today(),
        end_date=jdatetime.datetime.today() + jdatetime.timedelta(days=3),
        agency=faker.name(),
        price=faker.pyfloat(left_digits=10, right_digits=3),
    )


# @pytest.fixture
# def plane(db, user):
#     """Create Plance instance for testing"""
#     return Plane.objects.create(
#         user=user,
#         origin="1403-01-01",
#         destination="1403-01-04",
#     )


@pytest.fixture
def tourTicket(db, tour):
    """Create Ticket instance for testing"""

    return TourTicket.objects.create(
        tour=tour,
    )


@pytest.mark.django_db
class TestTicketModels:
    """Tests suite for ticket models"""

    # def testHotel(self, hotel):
    #     assert hotel.enter
    #     assert hotel.exit

    def testTour(self, tour):
        assert tour.user
        assert tour.image
        assert tour.info
        assert tour.origin
        assert tour.destination
        assert tour.rest_place
        assert tour.start_date
        assert tour.end_date
        assert tour.agency
        assert tour.price
        assert tour.slug

    # def testPlane(self, plane):
    #     assert plane.origin
    #     assert plane.destination

    def testTourTicket(self, tourTicket):
        assert tourTicket.tour.user
        assert tourTicket.tour.image
        assert tourTicket.tour.info
        assert tourTicket.tour.origin
        assert tourTicket.tour.destination
        assert tourTicket.tour.rest_place
        assert tourTicket.tour.start_date
        assert tourTicket.tour.end_date
        assert tourTicket.tour.agency
        assert tourTicket.tour.price

    def testTourFavorite(self, tourFavorite):
        assert tourFavorite.favorite.agency


@pytest.mark.django_db
class TestTicketViews:
    """Tests suite for tickets app views"""

    def testTourList(self, client):
        url = reverse("tour-list")
        resp = client.get(url)
        assert resp.status_code == 200

    def testTourByOrigin(self, client, tour):
        url = reverse("tour-list")
        resp = client.get(url, {"origin": tour.origin})
        assert resp.status_code == 200

    def testTourByDestination(self, client, tour):
        url = reverse("tour-list")
        resp = client.get(url, {"destination": tour.destination})
        assert resp.status_code == 200

    def testTourByOriginDestination(self, client, tour):
        url = reverse("tour-list")
        resp = client.get(
            url,
            {
                "origin": tour.origin,
                "destination": tour.destination,
            },
        )
        assert resp.status_code == 200

    def testTourInvalidOriginDestination(self, client):
        url = reverse("tour-list")
        resp = client.get(
            url,
            {
                "origin": "Invalid origin",
                "destination": "Invalid destination",
            },
        )
        assert resp.status_code == 200
        assert len(resp.data) == 0

    def testTourTicketList(self, client, jwt):
        access, refresh = jwt
        print("access ", access)
        print("refresh ", refresh)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("tour-ticket-list-create")
        resp = client.get(url)
        assert resp.status_code == 200

    def testTourTicketCreate(self, client, jwt, tour):
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("tour-ticket-list-create")
        resp = client.post(
            url,
            data={
                "tour": tour.id,
            },
        )
        assert resp.status_code == 201

    def testTourHistory(self, client, jwt):
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("tour-history")
        resp = client.get(url)

        assert resp.status_code == 200
