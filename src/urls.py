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
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import activate_user, custom_password_reset_confirm

handler_404 = "users.views.handler400"


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # Redirection
    path("", RedirectView.as_view(url="swagger/")),
    # drf-spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    # djoser
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include(("djoser.urls.jwt", "jwt"), namespace="jwt")),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        custom_password_reset_confirm,
        name="password_reset_confirm",
    ),
    path("activate/<uid>/<token>/", activate_user, name="activate-user"),
    path("", include("tickets.urls")),
    path("", include("trips.urls")),
]

urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
