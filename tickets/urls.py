from django.urls import path

from .views import *

urlpatterns = [
    path("tour-reserve/", TourReserveListCreateAPI.as_view(), name="tour_reserve"),
    path(
        "tour-reserve/<int:pk>/",
        TourReserveRetrieveDestroyAPI.as_view(),
        name="tour_reserve_detail",
    ),
    path(
        "tour-reserve-history/",
        TourReserveHistoryAPI.as_view(),
        name="tour_reserve_history",
    ),
    path("flight-ticket/", FlightTicketListCreateAPI.as_view(), name="flight_ticket"),
    path(
        "flight-ticket/<int:pk>/",
        FlightTicketRetrieveDestroyAPI.as_view(),
        name="flight_ticket_detail",
    ),
    path(
        "flight-ticket-history/",
        FlightTicketHistoryAPI.as_view(),
        name="flight_ticket_history",
    ),
    path("hotel-reserve/", HotelReserveListCreateAPI.as_view(), name="hotel_reserve"),
    path(
        "hotel-reserve/<int:pk>/",
        HotelReserveRetrieveDestroyAPI.as_view(),
        name="hotel_reserve_detail",
    ),
    path(
        "hotel-reserve-history/",
        HotelReserveHistoryAPI.as_view(),
        name="hotel_reserve_history",
    ),
]
