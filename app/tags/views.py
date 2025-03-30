from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from tags.models import Tag
from tags.serializers import TagSerializer


# NOTE: The approach customizes the accessibility, by:
#   - Using a GenericViewSet instead of ModelViewSet
#   - Using mixins to provide only the desired actions( UpdateModelMixin for update and ListModelMixin for list)
#   - Using a custom queryset to filter the tags to the authenticated user
class TagViewSet(
    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Manage tags in the database."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Replace the default queryset with a custom one
    # that filters the tags to the authenticated user
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
