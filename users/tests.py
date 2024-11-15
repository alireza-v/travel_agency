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
    return User.objects.create_user(
        email=faker.email(),
        password=faker.password(),
    )


@pytest.fixture
def client(db):
    return APIClient()


@pytest.mark.django_db
class TestUsersModels:
    """Test suite for users app models"""

    def testProfile(self, user):
        """Test Profile model"""
        assert user.email


@pytest.mark.django_db
class TestUsersViews:
    """Test suite for users app views"""

    @pytest.fixture
    def testRegister(self, db, client, user):
        """Test GET/POST registraton using using email and password"""
        url = reverse("register")
        respGet = client.get(url)
        respPost = client.post(
            url,
            data={
                "email": user.email,
                "password": user.password,
            },
        )

        assert respGet.status_code == 200
        assert respPost.status_code == 201

    @pytest.fixture
    def testLogin(self, client, user):
        """Test login or register using email and password and receiving accesss/refresh JWT token"""
        url = reverse("login")
        resp = client.post(
            url,
            {
                "email": user.email,
                "password": user.password,
            },
        )

        assert resp.status_code == 201
