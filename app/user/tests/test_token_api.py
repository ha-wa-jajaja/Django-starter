from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_LOGIN_URL = reverse("user_login")
ADMIN_LOGIN_URL = reverse("admin_login")
TOKEN_REFRESH_URL = reverse("token_refresh")

USER_INFO = {
    "email": "user@example.com",
    "password": "userpass123",
    "name":"Regular User"
}

ADMIN_INFO = {
    "email": "admin@example.com",
    "password": "adminpass123",
    "name": "Admin User"
}


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class JWTAuthApiTests(TestCase):
    """Test JWT auth features"""

    def setUp(self):
        self.client = APIClient()
        
        # Create regular user
        self.user = create_user(
            email=USER_INFO["email"],
            password=USER_INFO["password"],
            name=USER_INFO["name"],
        )
        
        # Create admin user
        self.admin = create_user(
            email=ADMIN_INFO["email"],
            password=ADMIN_INFO["password"],
            name=ADMIN_INFO["name"],
            is_staff=True,
        )

    def test_user_login(self):
        """Test generates token for valid credentials."""
       

        payload = {
            "email": USER_INFO["email"],
            "password": USER_INFO["password"],
        }
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_login_at_user_endpoint(self):
        """Test admin can also login at user endpoint."""
        payload = {
            "email": "admin@example.com",
            "password": "adminpass123",
        }
        res = self.client.post(USER_LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)

    def test_admin_login_success(self):
        """Test admin can login at admin endpoint."""
        payload = {
            "email": "admin@example.com",
            "password": "adminpass123",
        }
        res = self.client.post(ADMIN_LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertIn("is_staff", res.data)

    def test_regular_user_cannot_login_at_admin_endpoint(self):
        """Test regular user is denied at admin endpoint."""
        payload = {
            "email": "user@example.com",
            "password": "userpass123",
        }
        res = self.client.post(ADMIN_LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("access", res.data)

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
            USER_LOGIN_URL,
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
