"""
Tests for admin-only user API endpoints.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USERS_LIST_URL = reverse("user:admin_user_list")
TOKEN_URL = reverse("token_obtain_pair")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class AdminUserApiTests(TestCase):
    """Test admin-only API endpoints."""

    def setUp(self):
        # Create admin user
        self.admin_user = get_user_model().objects.create_user(
            email="admin@example.com",
            password="adminpass123",
            name="Admin User",
            is_staff=True,  # This makes the user an admin
        )

        # Create regular user
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com",
            password="userpass123",
            name="Regular User",
        )

        # Create API client
        self.client = APIClient()

    def test_list_users_admin_success(self):
        """Test admin can retrieve list of users successfully."""
        # Get JWT token for admin
        res = self.client.post(
            TOKEN_URL,
            {"email": "admin@example.com", "password": "adminpass123"},
        )
        token = res.data["access"]

        # Set admin credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test access to users list
        res = self.client.get(USERS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Check if the required fields are present in the response
        required_fields = ["id", "email", "name", "is_active", "is_staff"]

        # Check first user object in the list has all required fields
        user_data = res.data[0]
        for field in required_fields:
            self.assertIn(field, user_data)

    def test_list_users_regular_user_denied(self):
        """Test regular user cannot access users list."""
        # Get JWT token for regular user
        res = self.client.post(
            TOKEN_URL,
            {"email": "user@example.com", "password": "userpass123"},
        )
        token = res.data["access"]

        # Set regular user credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test access to users list
        res = self.client.get(USERS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
