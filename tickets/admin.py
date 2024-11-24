from django.contrib import admin

from .models import *


@admin.register(Tour)
class AdminTour(admin.ModelAdmin):
    list_display = ("origin", "destination", "info", "slug", "price")


@admin.register(TourTicket)
class AdminBookTour(admin.ModelAdmin):
    list_display = ["tour"]


@admin.register(Plane)
class AdminPlane(admin.ModelAdmin):
    list_display = ("origin", "destination")
