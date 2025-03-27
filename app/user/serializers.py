"""
Serializers for the user API View.
"""

from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# NOTE: This serializer works in both directions:
# 1. From Python to JSON: Serializes the data for the response
# 2. From JSON to Python: Deserializes the data for the request


# NOTE: serializers.ModelSerializer is a specialized serializer class that's tightly coupled to a Django model
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # NOTE: Meta class is crucial ModelSerializer because it provides the link to the model
    # And the relationship configuration
    class Meta:
        # NOTE: The model the get_user_model returns is the class User we defined in app\core\models\user.py
        # specified in app\app\settings.py #136
        model = get_user_model()

        # NOTE:  fields: specifies which model fields should be included in the serialization or deserialization process.
        fields = ["email", "password", "name"]
        # NOTE: extra_kwargs provides additional configuration options for fields that are defined in the fields attribute.
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # NOTE: The ModelSerializer already has a built-in create method,
    # but we override it here to handle the password hashing.
    def create(self, validated_data: Dict[str, Any]):
        """Create and return a user with encrypted password."""

        # Get values from validated_data with appropriate defaults
        email = validated_data.get("email")
        password = validated_data.get("password")
        name = validated_data.get("name", "")

        # NOTE: This create_user is defined in the UserManager in app/core/models/user.py
        return get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)

        # NOTE: super() refers to the parent class, which is serializers.ModelSerializer
        # .update() is built inside
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user info in response"""

    # Calls validate first, and get token
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional user profile data only needed at login
        # Will be returned with the token response
        # In this case:
        # {
        #   refresh: string
        #   access: string
        #   name: string
        #   email: string
        # }
        data["name"] = self.user.name
        data["email"] = self.user.email
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add essential data needed throughout the session to encode in the token
        token["user_id"] = user.id
        token["is_staff"] = user.is_staff  # Useful for permission checks
        return token
