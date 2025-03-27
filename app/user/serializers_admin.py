from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin views of user objects."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "is_active", "is_staff"]
