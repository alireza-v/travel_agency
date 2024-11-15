from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import to_python
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import is_valid_number
from rest_framework import serializers

from .models import *

User = get_user_model()


# class ProfileSer(serializers.ModelSerializer):
#     """Phone number serialization"""

#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ("email", "password")

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data.get("email"),
#             password=validated_data.get("password"),
#         )
#         return user


class LoginSer(serializers.Serializer):
    """Phone number serialization"""

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # def validate_phone_number(self, value):
    #     phone_number = to_python(value)
    #     if not phone_number or not is_valid_number(phone_number):
    #         raise serializers.ValidationError("Enter a valid phone number.")
    #     return value
