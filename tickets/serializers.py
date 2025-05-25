from typing import Any

from django.utils.dateformat import format
from rest_framework import serializers

from trips.serializers import *

from .models import *


class HistorySer(serializers.Serializer):
    id = serializers.IntegerField()
    deleted_on = serializers.DateTimeField(source="history_date")
    deleted_by = serializers.CharField(source="history_user.email", default="Unknown")


class TourReserveSer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    tour = serializers.SerializerMethodField()

    class Meta:
        model = TourReserve
        fields = ["id", "user", "tour"]

    def get_tour(self, obj):
        return {
            "id": obj.tour.id,
            "origin": obj.tour.origin,
            "destination": obj.tour.destination,
            "departure_time": obj.tour.departure_time,
            "arrival_time": obj.tour.arrival_time,
        }


class FlightTicketSer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    flight = FlightSer

    class Meta:
        model = FlightTicket
        fields = ["user", "flight"]


class HotelReserveSer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    hotel = HotelSer

    class Meta:
        model = HotelReserve
        fields = ["user", "hotel"]
