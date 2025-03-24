"""
Views for the user API.
"""
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # NOTE: serializer_class is a built-in attribute in Django REST Framework that specifies serializer for the view
    serializer_class = UserSerializer
