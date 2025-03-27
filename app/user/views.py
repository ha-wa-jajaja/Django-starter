"""
Views for the user API.
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserTokenObtainPairSerializer, UserSerializer


# NOTE: generics.CreateAPIView is Django REST Framework specified POST request handler.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # NOTE: serializer_class is a built-in attribute in Django REST Framework that specifies serializer for the view
    # 1. When a POST request arrives, CreateAPIView looks at the serializer_class
    # 2. Then it creates an instance of the UserSerializer and passes the request data to it.
    # 3. The serializer validates the data using definition from UserSerializer.Meta
    # 4. After validation, CreateAPIView calls serializer's save() method, which in turn calls the serializer's create() method
    # 5. Finally, the view returns an appropriate response
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    # NOTE: serializers are to handle interaction with the DB model
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # get_object() is a method defined within generics.RetrieveUpdateAPIView
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserTokenObtainPairView(TokenObtainPairView):
    """Custom token view using our serializer"""

    serializer_class = UserTokenObtainPairSerializer
