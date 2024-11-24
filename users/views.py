from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from djoser.utils import decode_uid
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

User = get_user_model()


def handler404(request, exception=None):
    """404 Response"""
    return JsonResponse(dict(message="Not found"), status=400)


def activate_user(request, uid, token):
    """Activate email"""
    try:
        uid = decode_uid(uid)
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(
            request,
            "users/activation_success.html",
            {
                "user": user,
            },
        )
    else:
        return HttpResponseBadRequest("Invalid activation link")


def custom_password_reset_confirm(request, uidb64, token):
    """Reset password confirmation"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponse("Password reset successful")
            else:
                return render(
                    request,
                    "users/custom_password_reset_confirm.html",
                    {
                        "validlink": True,
                        "error": "Passwords do not match",
                    },
                )
        return render(
            request,
            "users/custom_password_reset_confirm.html",
            {
                "validlink": True,
            },
        )
    return render(
        request,
        "users/custom_password_reset_confirm.html",
        {
            "validlink": False,
        },
    )


@extend_schema(
    summary="THIS VIEW FUNCTION IS FOR TESTING PURPOSES",
    description="THIS VIEW FUNCTION IS FOR TESTING PURPOSES",
    responses={
        200: UsersSer(many=True),
    },
)
class Users(generics.ListAPIView):
    """
    Display list of registered users and accessible only by admin
    ->->-> THIS VIEW FUNCTION IS FOR TESTING PURPOSES <-<-<-
    """

    permission_classes = [permissions.IsAdminUser]
    queryset = Profile.objects.all().order_by("-id")
    serializer_class = UsersSer
