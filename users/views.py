from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


def handler404(request, exception=None):
    return JsonResponse(dict(message="Not found"), status=400)


# @extend_schema(
#     summary="Profile registration using email and password",
#     description="Profile registration using email and password",
#     tags=["Auth"],
#     request={201:ProfileSer},
#     responses={200:ProfileSer},
# )
# class Register(generics.CreateAPIView):
#     """Profile registration using email and password"""

#     permission_classes = [permissions.AllowAny]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSer


@extend_schema(
    summary="Register/Login view using email and password",
    description="Register/Login view using email and password",
    tags=["Auth"],
    request={LoginSer},
    responses={201: LoginSer},
)
class Login(generics.CreateAPIView):
    """Register/Login view using email and password"""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSer

    def perform_create(self, serializer):
        """Using atomic transaction to roll back inserted data if any error occurs"""
        try:
            with transaction.atomic():
                email = serializer.validated_data.get("email")
                password = serializer.validated_data.get("password")

                user, created = Profile.objects.get_or_create(email=email)
                user.set_password(password)
                user.save()

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                if created:
                    message = render_to_string(
                        "users/account_activation_email.html",
                        {
                            "user": user,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": PasswordResetTokenGenerator().make_token(user),
                            "domain": get_current_site(self.request),
                        },
                    )
                    send_mail(
                        subject="Email confirmation link",
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=False,  # Any email errors trigger an exception
                        html_message=message,
                    )
                self.response_data = {
                    "refresh": str(refresh),
                    "access": access_token,
                    "message": "Login success"
                    if not created
                    else "Registration success",
                }
        except Exception as e:
            print(e)
            # return JsonResponse(dict(error="Something went wrong, please try again."))
            self.response_data = {"error": "Something went wrong, please try again."}
            raise  # Re-raise to trigger transaction rollback

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = self.response_data
            return response
        except Exception:
            return Response(
                self.response_data,
                400,
            )


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myUser = Profile.objects.get(pk=uid)
    except Profile.DoesNotExist:
        myUser = None

    if myUser is not None and PasswordResetTokenGenerator().check_token(myUser, token):
        myUser.email_is_verified = True
        myUser.save()
        return JsonResponse(dict(message="Your account has been activated!"))
    else:
        return JsonResponse(dict(error="Failed to activate the account"))
