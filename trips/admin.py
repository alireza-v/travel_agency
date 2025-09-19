from django.contrib import admin

from trips.models import Flight, Tour


@admin.register(Tour)
class AdminTour(admin.ModelAdmin):
    exclude = ["user", "slug"]
    list_display = ["origin", "destination", "departure_time", "arrival_time"]
    list_filter = ["origin"]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Flight)
class AdminPlane(admin.ModelAdmin):
    list_display = ["id", "user"]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
