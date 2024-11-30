from django.contrib import admin
from django.contrib.auth.models import Group

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
