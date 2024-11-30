import django_jalali.db.models as jmodels
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from tickets.models import *
from users.models import *

User = get_user_model()


class Tour(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tours")
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
    )

    origin = models.CharField(max_length=60, null=True, default="name_origin")
    destination = models.CharField(max_length=60, null=True, default="name_destination")
    description = models.TextField(
        verbose_name="describe tour features",
        default="describe tour features",
        unique=True,
    )
    rest_place = models.TextField(default="Name rest area")
    departure_time = models.DateField()
    arrival_time = models.DateField()
    agency = models.CharField(max_length=100, default="agency name")
    price = models.DecimalField(
        max_digits=13,
        decimal_places=3,
        default=99.9,
    )
    slug = models.SlugField(unique=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-timestamp"]

    def clean(self):
        """Image validation"""
        if self.image:
            if not self.image.name.endswith((".jpg", ".png")):
                raise ValidationError(
                    {"image": "Either only JPG or PNG file format accepted"}
                )

        """Time validation"""
        if self.departure_time == self.arrival_time:
            raise ValidationError(
                {
                    "arrival_time": "Departure time can not be the same as the arrival time"
                }
            )

        if (
            self.arrival_time < self.departure_time
            or self.departure_time > self.arrival_time
        ):
            raise ValidationError(
                {
                    "arrival_time": "Tour timing mismatch",
                }
            )

        super().clean()

    def __str__(self):
        return f"{self.origin}-> {self.destination}"

    def duration(self):
        """Total time spent for a tour"""
        if self.departure_time and self.arrival_time:
            difference = self.arrival_time - self.departure_time
            return f"{difference.days} nights"
        return None

    def save(self, *args, **kwargs):
        """tour description as slug"""
        if not self.slug:
            self.slug = slugify(self.description)

        super().save(*args, **kwargs)


class Flight(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flights")
    origin = models.CharField(max_length=60, null=True, default="Flight origin")
    destination = models.CharField(
        max_length=60, null=True, default="Flight destination"
    )
    departure_time = models.DateField()
    arrival_time = models.DateField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default="99.0")
    agency = models.CharField(max_length=100, default="Enter agency name", null=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.origin}-> {self.destination}"

    def clean(self):
        """
        Ensure origin and destination be different
        Ensure departure time precedes the arrival time
        """
        if self.origin == self.destination:
            raise ValidationError("Origin and Destination can not be the same")

        if (
            self.departure_time >= self.arrival_time
            or self.arrival_time < self.departure_time
        ):
            raise ValidationError("Time mismatch")


class Hotel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    destination = models.CharField(
        max_length=60, null=True, default="hotel destination"
    )
    arrival_time = models.DateField(null=True)
    departure_time = models.DateField(null=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.arrival_time}-> {self.departure_time}"
