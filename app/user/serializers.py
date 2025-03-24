"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model
from typing import Dict, Any

from rest_framework import serializers

# NOTE: This serializer works in both directions:
# 1. From Python to JSON: Serializes the data for the response
# 2. From JSON to Python: Deserializes the data for the request
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()

        # NOTE:  fields: specifies which model fields should be included in the serialization or deserialization process.
        fields = ['email', 'password', 'name']
        # NOTE: extra_kwargs provides additional configuration options for fields that are defined in the fields attribute.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data: Dict[str, Any]):
        """Create and return a user with encrypted password."""

        # Get values from validated_data with appropriate defaults
        email = validated_data.get('email')
        password = validated_data.get('password')
        name = validated_data.get('name', '')


        # NOTE: This create_user is defined in the UserManager in app/core/models/user.py
        return get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )
