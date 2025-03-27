from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers_admin import AdminUserSerializer


class AdminListUsersView(generics.ListAPIView):
    """List all users - admin only endpoint."""

    serializer_class = AdminUserSerializer
    authentication_classes = [JWTAuthentication]

    # NOTE: permissions.IsAdminUser is a DRF built-in permission class
    # that checks if the requesting user's is_staff attribute is True
    permission_classes = [permissions.IsAdminUser]

    queryset = get_user_model().objects.all()


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve or update a specific user - admin only endpoint."""

    serializer_class = AdminUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    # Get the User model that's defined in settings.AUTH_USER_MODEL
    queryset = get_user_model().objects.all()

    # The lookup field is 'id' by default, but explicitly specify
    lookup_field = "pk"  # primary key, which is the 'id'
