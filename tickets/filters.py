import django_filters

from .models import *


class TourFilter(django_filters.FilterSet):
    location = django_filters.ChoiceFilter(choices=CityChoices.choices)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Tour
        fields = ["location", "min_price", "max_price"]
