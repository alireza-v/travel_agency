"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tickets.views import *
from users.views import *

handler_404 = "users.views.handler400"


urlpatterns = [
    path("admin/", admin.site.urls),
    # Redirection
    path("", RedirectView.as_view(url="swagger/")),
    # drf-spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # users app
    # path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("activate/<uidb64>/<token>", activate_account, name="activate"),
    # tickets app
    path("tours/", TourList.as_view(), name="tour-list"),
    path("tours/<slug:slug>/", TourRetrieve.as_view(), name="tour-retrieve"),
    path(
        "tour/ticket/",
        TourTicketListCreateView.as_view(),
        name="tour-ticket-list-create",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
