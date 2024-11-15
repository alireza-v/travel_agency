from typing import Any

from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from rest_framework import serializers

from .models import *


class TourSer(serializers.ModelSerializer):
    # user = serializers.EmailField()
    origin = serializers.CharField(source="get_origin_display", read_only=True)
    destination = serializers.CharField(
        source="get_destination_display", read_only=True
    )

    start_date = JDateField()
    end_date = JDateField()

    duration = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "origin",
            "destination",
            "image",
            "info",
            "duration",
            "rest_place",
            "start_date",
            "end_date",
            "agency",
            "price",
            # "destination",
            # "origin",
            # "user",
            # "slug",
        ]

    def get_duration(self, obj: Any) -> str:
        return obj.duration()

    def create(self, validated_data):
        email = validated_data.pop("user")
        user = Profile.objects.get(email=email)
        tour = Tour.objects.create(user=user, **validated_data)
        return tour


class TourTicketSer(serializers.ModelSerializer):
    tour = TourSer

    class Meta:
        model = TourTicket
        fields = [
            "tour",
        ]
