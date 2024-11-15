# from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import *
from .tokens import *

User = get_user_model()


# @receiver(post_save, sender=User)
# def sendMailActivationLink(sender, instance, created, **kwargs):
#     if created:
#         print("Signal created hence sending mail confirmation")
#         try:
#             with transaction.atomic():
#                 message = render_to_string(
#                     "users/account_activation_email.html",
#                     {
#                         "user": instance,
#                         "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
#                         "token": PasswordResetTokenGenerator().make_token(instance),
#                         # "domain":Site.objects.get_current()
#                     },
#                 )
#                 send_mail(
#                     subject="Email confirmation link",
#                     message=message,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[instance.email],
#                     fail_silently=False,  # Any email errors trigger an exception
#                     html_message=message,
#                 )
#         except Exception as e:
#             print("Error occured while sending mail")
