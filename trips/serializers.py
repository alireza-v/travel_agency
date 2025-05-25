from typing import Any

from rest_framework import serializers

from .models import *


class TourSer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "origin",
            "destination",
            "image",
            "description",
            "duration",
            "rest_place",
            "departure_time",
            "arrival_time",
            "agency",
            "price",
        ]

    def get_duration(self, obj: Any) -> str:
        return obj.duration()


class FlightSer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ["timestamp", "updated", "user"]


class HotelSer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
