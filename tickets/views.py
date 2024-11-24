from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Create your views here.
from rest_framework import filters, generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .filters import *
from .serializers import *


@extend_schema(
    summary="Available tours",
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
    summary="Tour detail",
    description="Retrieve the tour instance using the slug field",
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TourSer

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Tour, slug=slug)


@extend_schema(
    summary="Old tours",
    description="Display history of deleted tours",
    responses={
        200: TourHistSer(many=True),
    },
)
class TourHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TourHistSer

    def get_queryset(self):
        queryset = (
            Tour.history.filter(history_type="-")
            .annotate(
                deleted_by=F("history_user__email"),
            )
            .order_by("-history_date")
        )
        return queryset


class TourTicketListCreate(generics.ListCreateAPIView):
    """Display and Create tour ticket"""

    permission_classes = [permissions.IsAuthenticated]
    queryset = TourTicket.objects.all().order_by("-timestamp")
    serializer_class = TourTicketSer

    @extend_schema(
        summary="Tour tickets",
        description="Display bought tour tickets",
        responses={
            200: TourTicketSer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Buy ticket",
        description="Buy ticket from the available tours",
        request=TourTicketSer,
        responses={
            201: TourTicketSer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
