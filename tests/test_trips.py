from .conftest import *


@pytest.mark.django_db
class TestTripsModels(BaseTest):
    """
    trips models
    test suite covers:
        - model field validations
        - related model behaviors
    """

    def test_tour(self):
        assert self.tour.user
        assert self.tour.origin
        assert self.tour.destination

    def test_flight(self):
        assert self.flight.origin
        assert self.flight.destination
        assert self.flight.departure_time
        assert self.flight.arrival_time
        assert self.flight.ticket_price
        assert self.flight.agency
        assert str(self.flight) == f"{self.flight.origin}-> {self.flight.destination}"

    def test_hotel(self):
        assert self.hotel.user
        assert self.hotel.destination
        assert self.hotel.arrival_time
        assert self.hotel.departure_time
        assert (
            str(self.hotel)
            == f"{self.hotel.arrival_time}-> {self.hotel.departure_time }"
        )


@pytest.mark.django_db
class TestTripsViews(BaseTest):
    """
    trips views
    test suite covers:
        - list/create view responses
        - retrieve/destroy method
        - history/filtering responses

    """

    def test_tour_list(self):
        url = reverse("tours")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_tour_search(self):
        url = reverse("tours")
        resp = self.client.get(url, {"search": "shiraz"})
        assert resp.status_code == 200

    def test_tour_detail(self):
        url = reverse("tour_detail", kwargs={"slug": self.tour.slug})
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_flight_list(self):
        url = reverse("flights")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_flight_detail(self):
        url = reverse(
            "flight_detail",
            kwargs={
                "pk": self.flight.pk,
            },
        )
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_flight_search(self):
        url = reverse("flights")
        resp = self.client.get(
            url,
            {
                "search": "tehran",
            },
        )
        assert resp.status_code == 200

    def test_hotel_list(self):
        url = reverse("hotels")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_hotel_detail(self):
        url = reverse(
            "hotel_detail",
            kwargs={
                "pk": self.hotel.pk,
            },
        )
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_hotel_search(self):
        url = reverse("hotels")
        resp = self.client.get(
            url,
            {
                "search": self.hotel.destination,
            },
        )
        assert resp.status_code == 200
