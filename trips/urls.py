from django.urls import path

from trips.views import (
    FlightDetailAPI,
    FlightListAPI,
    HotelDetailAPI,
    HotelListAPI,
    TourDetailAPI,
    TourListAPI,
)

urlpatterns = [
    path("tours/", TourListAPI.as_view(), name="tours"),
    path("tours/<slug:slug>/", TourDetailAPI.as_view(), name="tour_detail"),
    path("flights/", FlightListAPI.as_view(), name="flights"),
    path("flights/<int:pk>/", FlightDetailAPI.as_view(), name="flight_detail"),
    path("hotels/", HotelListAPI.as_view(), name="hotels"),
    path("hotel/<int:pk>/", HotelDetailAPI.as_view(), name="hotel_detail"),
]
