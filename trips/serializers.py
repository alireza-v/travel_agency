from typing import Any

from rest_framework import serializers

from .models import *


class TourSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = "__all__"

    def get_duration(self, obj: Any) -> str:
        return obj.duration()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ["timestamp", "updated", "user"]


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
