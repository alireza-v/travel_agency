from django.urls import path

from .views import *

urlpatterns = [
    path("tours/", TourList.as_view(), name="tour-list"),
    path("tours/<slug:slug>/", TourRetrieve.as_view(), name="tour-retrieve"),
    path(
        "tour/ticket/",
        TourTicketListCreate.as_view(),
        name="tour-ticket-list-create",
    ),
    path("tour-histo/", TourHistoryView.as_view(), name="tour-history"),
]
