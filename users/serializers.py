from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

from .models import *

User = get_user_model()


class CustomUserSer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "email", "is_active"]
