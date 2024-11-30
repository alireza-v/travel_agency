from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from djoser.utils import decode_uid

from .serializers import *

User = get_user_model()


def handler404(request, exception=None):
    """404 Response"""
    return JsonResponse(dict(message="Not found"), status=400)


def activate_user(request, uid, token):
    """Activate user email address"""
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
