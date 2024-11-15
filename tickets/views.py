from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Create your views here.
from rest_framework import filters, generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .filters import *
from .serializers import *


@extend_schema(
    summary="Display the available tours",
    description="Display the available tours",
    tags=["Tours"],
    responses={200: TourSer},
)
class TourList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Tour.objects.all().order_by("-id")
    serializer_class = TourSer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        origin_query = self.request.query_params.get("origin", "").strip()
        destination_query = self.request.query_params.get("destination", "").strip()

        city_choices = {v.lower(): k for k, v in dict(CityChoices.choices).items()}

        if origin_query:
            origin_id = city_choices.get(origin_query.lower())
            if origin_id is not None:
                queryset = queryset.filter(origin=origin_id)
            else:
                return queryset.none()

        if destination_query:
            destination_id = city_choices.get(destination_query.lower())
            if destination_id is not None:
                queryset = queryset.filter(destination=destination_id)
            else:
                return queryset.none()

        return queryset


@extend_schema(
    summary="Retrieve Tour instance through the slug field",
    description="Retrieve Tour instance through the slug field",
    tags=["Tours"],
    responses={
        200: TourSer,
        404: OpenApiResponse(description="Tour not found"),
    },
    parameters=[
        OpenApiParameter(
            name="slug",
            type=str,
            description="The unique slug of the tour",
            required=True,
        )
    ],
)
class TourRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Tour.objects.all()
    serializer_class = TourSer

    def get_object(self):
        slug = self.kwargs.get("slug")

        try:
            return Tour.objects.get(slug=slug)
        except Tour.DoesNotExist:
            raise Http404("Tour not found")


class TourTicketListCreateView(generics.ListCreateAPIView):
    """Display and Create ticket for the available tours"""

    permission_classes = [permissions.IsAuthenticated]
    queryset = TourTicket.objects.all().order_by("-timestamp")
    serializer_class = TourTicketSer

    @extend_schema(
        summary="Display user bought tickets",
        description="Display bought tickets",
        responses={
            200: TourTicketSer(many=True),
        },
        parameters=[],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Buy ticket from the available tours",
        description="Buy ticket from the available tours",
        request=TourTicketSer,
        responses={
            201: TourTicketSer,
        },
        parameters=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
