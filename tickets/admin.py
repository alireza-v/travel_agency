from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Tour)
class AdminTour(admin.ModelAdmin):
    list_display = ("origin", "destination", "info", "slug", "price")


@admin.register(TourTicket)
class AdminBookTour(admin.ModelAdmin):
    list_display = ["number", "tour"]


# @admin.register(Plane)
# class AdminPlane(admin.ModelAdmin):
# list_display = ("origin", "destination")
