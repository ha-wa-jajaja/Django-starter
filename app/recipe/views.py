"""
Views for the recipe APIs
"""

from recipe import serializers
from recipe.models import Recipe
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# NOTE: viewsets.ModelViewSet automatically provides a complete set of CRUD
# List (GET /recipes/): Returns all recipes for the authenticated user
# Create (POST /recipes/): Creates a new recipe
# Retrieve (GET /recipes/{id}/): Returns a specific recipe
# Update (PUT/PATCH /recipes/{id}/): Updates a specific recipe
# Destroy (DELETE /recipes/{id}/): Deletes a specific recipe
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    # Assign a default serializer class
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # NOTE: JWT authentication flow auto retrieves the full user object
        # using the user ID that's encoded in the token, result in self.request.user
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # NOTE: self.action == 'list' condition is triggered
        # when a GET request is made to the collection endpoint (without an ID).
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    # NOTE: perform_create method is called during the POST processing flow in DRF;
    # Runs after data validation and before saving the data to the database.

    # NOTE: This pattern is common in DRF when creating resources that belong to users:
    # doesn't accept a user field from clients, but instead assigns the user field
    # to the authenticated user that made the request.
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
