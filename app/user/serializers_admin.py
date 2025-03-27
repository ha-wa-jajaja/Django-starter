from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import PermissionDenied



class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Token serializer for admin users only"""

    def validate(self, attrs):
        # First call the parent's validate method
        data = super().validate(attrs)
        
        # Check if the authenticated user is an admin
        if not self.user.is_staff:
            raise PermissionDenied("Not authorized as admin")
            
        # Add additional admin profile data
        data["name"] = self.user.name
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff
        
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add essential data to token
        token["user_id"] = user.id
        token["is_staff"] = user.is_staff
        return token

class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin views of user objects."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "is_active", "is_staff"]
