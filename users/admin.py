from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ("email", "is_superuser")
    fieldsets = [
        (
            "Section title",
            {
                "classes": ("collapse", "expanded"),
                "fields": ("email", "email_is_verified"),
            },
        ),
    ]
