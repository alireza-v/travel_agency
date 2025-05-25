from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

# Create your views here.
from rest_framework import filters, generics, permissions

from .serializers import *


@extend_schema(summary="Tours", responses={200: TourSerializer(many=True)})
class TourListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["origin", "destination"]


@extend_schema(summary="Tour detail", responses={200: TourSerializer})
class TourDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TourSerializer

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Tour, slug=slug)


@extend_schema(summary="Flights", responses={200: FlightSerializer(many=True)})
class FlightListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["origin", "destination"]


@extend_schema(summary="Flight detail", responses={200: FlightSerializer})
class FlightDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


@extend_schema(summary="Hotels", responses={200: HotelSerializer})
class HotelListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["destination"]


@extend_schema(summary="Hotel detail", responses={200: HotelSerializer})
class HotelDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
