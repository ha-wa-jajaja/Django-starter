"""
Serializers for the user API View.
"""
from django.contrib.auth import (get_user_model, authenticate)
from typing import Dict, Any

from rest_framework import serializers

from django.utils.translation import gettext as _

# NOTE: This serializer works in both directions:
# 1. From Python to JSON: Serializes the data for the response
# 2. From JSON to Python: Deserializes the data for the request

# NOTE: serializers.ModelSerializer is a specialized serializer class that's tightly coupled to a Django model
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    #NOTE: Meta class is crucial ModelSerializer because it provides the link to the model
    # And the relationship configuration
    class Meta:
        # NOTE: The model the get_user_model returns is the class User we defined in app\core\models\user.py
        # specified in app\app\settings.py #136
        model = get_user_model()

        # NOTE:  fields: specifies which model fields should be included in the serialization or deserialization process.
        fields = ['email', 'password', 'name']
        # NOTE: extra_kwargs provides additional configuration options for fields that are defined in the fields attribute.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    #NOTE: The ModelSerializer already has a built-in create method,
    # but we override it here to handle the password hashing.
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
    
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)

        # NOTE: super() refers to the parent class, which is serializers.ModelSerializer
        # .update() is built inside
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    # NOTE: These two lines declares what data AuthTokenSerializer should expect when receives a request.
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""

        email = attrs.get('email')
        password = attrs.get('password')

        # NOTE: authenticate() is to verify a user's credentials
        # And returns the corresponding User object or None(if no user matches)
        user = authenticate(
            #NOTE: self.context is a dictionary that is made available to a serializer's methods
            #  during the serialization/deserialization process.

            # NOTE:Even if a simple username/password check doesn't need the request, 
            # including it maintains consistency in how authenticate() is called across different scenarios
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        return {'user': user}

        # NOTE: Course return attrs, but not needed
        # attrs['user'] = user
        # return attrs
