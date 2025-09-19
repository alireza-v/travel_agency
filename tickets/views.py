from django.db.models import F
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from tickets.models import FlightTicket, HotelReserve, TourReserve
from tickets.serializers import (
    FlightTicketSer,
    HistorySer,
    HotelReserveSer,
    TourReserveSer,
)


@extend_schema(
    summary="List/Create tour_reservation",
    responses={200: TourReserveSer(many=True)},
    request={201: TourReserveSer},
)
class TourReserveListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TourReserve.objects.all()
    serializer_class = TourReserveSer

    def perform_create(self, serializer):
        """
        Ensures that the user who sent the request is associated with the newly created `TourReserve`.
        """

        serializer.save(user=self.request.user)


@extend_schema(summary="Retrieve/Destroy the tour-reservation object")
class TourReserveRetrieveDestroyAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TourReserve.objects.all()
    serializer_class = TourReserveSer


@extend_schema(summary="history of deleted/canceled tour-reservatons")
class TourReserveHistoryAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistorySer

    def get_queryset(self):
        queryset = (
            TourReserve.history.filter(history_type="-")
            .annotate(
                deleted_by=F("history_user__email"),
            )
            .order_by("-history_date")
        )
        return queryset


@extend_schema(
    summary="List/Create flight tickets",
    responses={200: FlightTicketSer(many=True)},
    request={201: FlightTicketSer},
)
class FlightTicketListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FlightTicket.objects.all()
    serializer_class = FlightTicketSer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Retrieve/Destroy flight ticket object",
    request=FlightTicketSer,
    responses=FlightTicketSer,
)
class FlightTicketRetrieveDestroyAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FlightTicket.objects.all()
    serializer_class = FlightTicketSer


@extend_schema(summary="History of deleted flight tickets", responses={200: HistorySer})
class FlightTicketHistoryAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FlightTicketSer

    def get_queryset(self):
        queryset = (
            FlightTicket.history.filter(history_type="-")
            .annotate(
                deleted_by=F("history_user__email"),
            )
            .order_by("-history_date")
        )
        return queryset


@extend_schema(
    summary="List/Create hotel reservations",
    responses={200: HotelReserveSer(many=True)},
    request={201: HotelReserveSer},
)
class HotelReserveListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = HotelReserve.objects.all()
    serializer_class = HotelReserveSer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Retrieve/Destroy hotel reservation object",
    request=HotelReserveSer,
    responses=HotelReserveSer,
)
class HotelReserveRetrieveDestroyAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = HotelReserve.objects.all()
    serializer_class = HotelReserveSer


@extend_schema(
    summary="List hotel reserved history",
    responses={200: HotelReserveSer},
)
class HotelReserveHistoryAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistorySer

    def get_queryset(self):
        queryset = (
            HotelReserve.history.filter(history_type="-")
            .annotate(
                deleted_by=F("history_user__email"),
            )
            .order_by("-history_date")
        )
        return queryset
