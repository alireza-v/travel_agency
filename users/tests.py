# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

from .models import *

User = get_user_model()
faker = Faker()


@pytest.fixture
def user(db):
    email = "test@email.com"
    password = "1234QWqw"
    return User.objects.create_user(
        email=email,
        password=password,
    )


@pytest.fixture
def client(db):
    return APIClient()


@pytest.mark.django_db
class TestUserModel:
    """Test suite for user models"""

    def testProfile(self, user):
        assert user.email
        assert user.password


# @pytest.mark.django_db
# class TestUsersViews:
#     """Test suite for user views"""

#     @pytest.fixture
#     def testRegister(self, db, client, user):
#         """Test GET/POST registraton using using email and password"""
#         url = reverse("auth/register")
#         resp = client.post(
#             url,
#             data={
#                 "email": user.email,
#                 "password": user.password,
#             },
#         )
#         assert resp.status_code == 201

#     @pytest.fixture
#     def testLogin(self, client, user):
#         """Test login or register using email and password and receiving accesss/refresh JWT token"""
#         url = reverse("access-token")
#         resp = client.post(
#             url,
#             {
#                 "email": user.email,
#                 "password": user.password,
#             },
#         )

#         assert resp.status_code == 200
