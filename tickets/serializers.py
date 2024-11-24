from typing import Any

from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from rest_framework import serializers

from .models import *


class TourSer(serializers.ModelSerializer):
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
            "slug",
        ]

    def get_duration(self, obj: Any) -> str:
        return obj.duration()


class TourHistSer(serializers.Serializer):
    id = serializers.IntegerField()
    deleted_on = serializers.DateTimeField(source="history_date")
    deleted_by = serializers.CharField(source="history_user.email", default="Unknown")
    agency = serializers.CharField()
    origin = serializers.CharField(source="get_origin_display")
    destination = serializers.CharField(source="get_destination_display")
    info = serializers.CharField()
    start_date = JDateField()
    end_date = JDateField()


class TourTicketSer(serializers.ModelSerializer):
    tour = TourSer

    class Meta:
        model = TourTicket
        fields = [
            "tour",
        ]
