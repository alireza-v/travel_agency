import pytest
from django.urls import reverse

from conftest import BaseTest


@pytest.mark.django_db
class TestTicketsModels(BaseTest):
    """
    tickets models
    test suite covers:
        - related model behaviors
        - model field validations
    """

    def test_tour_reservation(self):
        assert self.tour_reservation.user
        assert self.tour_reservation.tour
        assert (
            str(self.tour_reservation)
            == f"{self.tour.origin}-> {self.tour.destination}"
        )

    def test_flight_ticket(self):
        assert self.flight_ticket.user
        assert self.flight_ticket.flight
        assert (
            str(self.flight_ticket)
            == f"{self.flight.origin}-> {self.flight.destination}"
        )

    def test_hotel_reservation(self):
        assert self.hotel_reservation.user
        assert self.hotel_reservation.hotel
        assert str(self.hotel_reservation) == self.hotel.destination


@pytest.mark.django_db
class TestTicketsViews(BaseTest):
    """
    tickets views
    test suite covers:
        - list/create view responses
        - retrieve/destroy method
        - history/filtering responses
    """

    @pytest.fixture
    def test_tour_reserve(self):
        url = reverse("tour_reserve")
        resp = self.client.get(url)
        resp_post = (
            self.client.post(
                url,
                data={
                    "tour": self.tour.pk,
                },
            ),
        )
        assert resp.status_code == 200
        assert resp_post.status_code == 201

    def test_tour_reserve_detail(self):
        url = reverse(
            "tour_reserve_detail",
            kwargs={
                "pk": self.tour_reservation.pk,
            },
        )
        resp = self.client.get(url)
        resp_del = self.client.delete(url)
        assert resp.status_code == 200
        assert resp_del.status_code == 204

    def test_tour_reserve_history(self):
        url = reverse("tour_reserve_history")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_flight_ticket(self):
        url = reverse("flight_ticket")
        resp = self.client.get(url)
        resp_post = self.client.post(
            url,
            data={
                "flight": self.flight.pk,
            },
        )
        assert resp.status_code == 200
        assert resp_post.status_code == 201

    def test_flight_ticket_detail(self):
        url = reverse(
            "flight_ticket_detail",
            kwargs={
                "pk": self.flight_ticket.pk,
            },
        )
        resp = self.client.get(url)
        resp_del = self.client.delete(url)
        assert resp.status_code == 200
        assert resp_del.status_code == 204

    def test_flight_ticket_history(self):
        url = reverse("flight_ticket_history")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_hotel_reserve(self):
        url = reverse("hotel_reserve")
        resp = self.client.get(url)
        resp_post = self.client.post(
            url,
            data={
                "hotel": self.hotel.pk,
            },
        )
        assert resp.status_code == 200
        assert resp_post.status_code == 201

    def test_hotel_reserve_detail(self):
        url = reverse(
            "hotel_reserve_detail",
            kwargs={
                "pk": self.hotel_reservation.pk,
            },
        )
        resp = self.client.get(url)
        resp_del = self.client.delete(url)
        assert resp.status_code == 200
        assert resp_del.status_code == 204

    def test_hotel_reserve_history(self):
        url = reverse("hotel_reserve_history")
        resp = self.client.get(url)
        assert resp.status_code == 200
