from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from trips.models import *
from users.models import *

User = get_user_model()


class TourReserve(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tour_reserve_user"
    )
    tour = models.OneToOneField(
        Tour, on_delete=models.CASCADE, related_name="tour_reserve"
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.tour.origin}-> {self.tour.destination}"


class FlightTicket(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="flight_ticket_user"
    )
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="flight_ticket"
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.flight.origin}-> {self.flight.destination}"


class HotelReserve(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hotel_reserve_user"
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="hotel_reserve"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.hotel.destination
