import random

import django_jalali.db.models as jmodels
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from users.models import *


class CityChoices(models.IntegerChoices):
    SHIRAZ = 1, "shiraz"
    TEHRAN = 2, "tehran"
    Isfahan = 3, "esfahan"
    Hamedan = 4, "hamedan"


class Tour(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tours")
    image = models.ImageField(upload_to="images/", null=True)
    info = models.TextField(default="Describe tour features", null=True, unique=True)
    origin = models.IntegerField(choices=CityChoices.choices, null=True)
    destination = models.IntegerField(choices=CityChoices.choices)
    rest_place = models.TextField(default="Name hotel for staying", null=True)
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    agency = models.CharField(max_length=50, default="Enter your agency", null=True)
    price = models.DecimalField(
        max_digits=13, decimal_places=3, default=12000000, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    history = HistoricalRecords()

    def clean(self):
        """Validate the image file format"""
        if self.image:
            if not self.image.name.endswith((".jpg", ".png")):
                raise ValidationError(_("Image must be in JPG or PNG format"))
        super().clean()

    def __str__(self):
        return f"{self.get_origin_display()}-> {self.get_destination_display()}"

    def duration(self):
        """Total time to be spent for a tour"""
        if self.start_date and self.end_date:
            difference = self.end_date - self.start_date
            return f"{difference.days} nights"
        return None

    def save(self, *args, **kwargs):
        """Slug: info field be used as a slug"""
        if not self.slug:
            self.slug = slugify(self.info)
        super().save(*args, **kwargs)


class TourTicket(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tour = models.OneToOneField(
        Tour, on_delete=models.CASCADE, related_name="tourTickets"
    )

    def __str__(self):
        return self.tour.get_origin_display()


class Plane(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="planes")
    origin = models.IntegerField(choices=CityChoices.choices)
    destination = models.IntegerField(choices=CityChoices.choices)

    def __str__(self):
        return f"{self.origin}-> {self.destination}"


class Hotel(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="hotels")
    enter = models.DateTimeField()
    exit = models.DateTimeField()

    def __str__(self):
        return f"{self.enter}-> {self.exit}"
