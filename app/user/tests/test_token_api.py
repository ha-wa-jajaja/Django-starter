from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

TOKEN_URL = reverse("token_obtain_pair")
TOKEN_REFRESH_URL = reverse("token_refresh")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class JWTAuthApiTests(TestCase):
    """Test JWT auth features"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        """Test refresh token endpoint."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        # First get tokens
        auth_res = self.client.post(
            TOKEN_URL,
            {
                "email": user_details["email"],
                "password": user_details["password"],
            },
        )
        refresh_token = auth_res.data["refresh"]

        # Test refresh endpoint
        res = self.client.post(TOKEN_REFRESH_URL, {"refresh": refresh_token})

        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
