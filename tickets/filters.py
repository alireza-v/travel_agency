from django_filters import ChoiceFilter, FilterSet, NumberFilter

from .models import *


class TourFilter(FilterSet):
    location = ChoiceFilter(choices=CityChoices.choices)
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Tour
        fields = ["location", "min_price", "max_price"]
