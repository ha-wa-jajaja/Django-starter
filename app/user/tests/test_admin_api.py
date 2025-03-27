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

    def detail_url(self, user_id):
        """Create and return a user detail URL."""
        return reverse("user:admin_user_detail", args=[user_id])

    def test_retrieve_user_admin_success(self):
        """Test admin can retrieve a user by ID successfully."""
        # Get JWT token for admin
        res = self.client.post(
            TOKEN_URL,
            {"email": "admin@example.com", "password": "adminpass123"},
        )
        token = res.data["access"]

        # Set admin credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test retrieving the regular user by ID
        url = self.detail_url(self.regular_user.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Check if response contains expected fields
        self.assertEqual(res.data["email"], self.regular_user.email)
        self.assertEqual(res.data["name"], self.regular_user.name)

    def test_update_user_admin_success(self):
        """Test admin can update a user by ID successfully."""
        # Get JWT token for admin
        res = self.client.post(
            TOKEN_URL,
            {"email": "admin@example.com", "password": "adminpass123"},
        )
        token = res.data["access"]

        # Set admin credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Update data for regular user
        payload = {"name": "Updated Name", "is_active": False}

        # Test updating the regular user by ID
        url = self.detail_url(self.regular_user.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh user from database
        self.regular_user.refresh_from_db()

        # Check if user was updated correctly
        self.assertEqual(self.regular_user.name, payload["name"])
        self.assertEqual(self.regular_user.is_active, payload["is_active"])

    def test_retrieve_update_user_forbidden_for_regular_user(self):
        """Test regular user cannot retrieve or update other users."""
        # Get JWT token for regular user
        res = self.client.post(
            TOKEN_URL,
            {"email": "user@example.com", "password": "userpass123"},
        )
        token = res.data["access"]

        # Set regular user credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Create another regular user to try to access
        another_user = create_user(
            email="another@example.com",
            password="anotherpass123",
            name="Another User",
        )

        # Try to retrieve the other user
        url = self.detail_url(another_user.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Try to update the other user
        res = self.client.patch(url, {"name": "Hacked Name"})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_admin_success(self):
        """Test admin can delete a user by ID successfully."""
        # Get JWT token for admin
        res = self.client.post(
            TOKEN_URL,
            {"email": "admin@example.com", "password": "adminpass123"},
        )
        token = res.data["access"]

        # Set admin credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test deleting the regular user by ID
        url = self.detail_url(self.regular_user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # Check if user was actually deleted from database
        self.assertFalse(
            get_user_model().objects.filter(id=self.regular_user.id).exists()
        )

    def test_delete_user_forbidden_for_regular_user(self):
        """Test regular user cannot delete other users."""
        # Get JWT token for regular user
        res = self.client.post(
            TOKEN_URL,
            {"email": "user@example.com", "password": "userpass123"},
        )
        token = res.data["access"]

        # Set regular user credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Create another regular user to try to delete
        another_user = create_user(
            email="another@example.com",
            password="anotherpass123",
            name="Another User",
        )

        # Try to delete the other user
        url = self.detail_url(another_user.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Verify user was not deleted
        self.assertTrue(get_user_model().objects.filter(id=another_user.id).exists())
