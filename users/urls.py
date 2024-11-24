from django.urls import path

from .views import *

urlpatterns = [
    path("users-list/", Users.as_view(), name="user-list"),
]
