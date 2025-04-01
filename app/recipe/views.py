"""
Views for the recipe APIs
"""

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from recipe import serializers
from recipe.models import Recipe
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter",
            ),
            OpenApiParameter(
                "ingredients",
                OpenApiTypes.STR,
                description="Comma separated list of ingredient IDs to filter",
            ),
            OpenApiParameter(
                "name",
                OpenApiTypes.STR,
                description="Name of the recipe to filter",
            ),
        ]
    )
)
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

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(title__icontains=name)
        if tags:
            tag_ids = self._params_to_ints(tags)
            # tags__id__in breaks down as:
            # tags: Refers to a model, in this case to tags.Tag
            # __id: This specifies that we want to filter by the id field of the related Tags model
            # __in: This is a lookup type that checks if the value is in a list or iterable
            # Django's way of handling SQL queries like: WHERE tags.id IN (1, 2, 3)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # NOTE: JWT authentication flow auto retrieves the full user object
        # using the user ID that's encoded in the token, result in self.request.user
        return queryset.filter(user=self.request.user).order_by("-id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # NOTE: self.action == 'list' condition is triggered
        # when a GET request is made to the collection endpoint (without an ID).
        if self.action == "list":
            return serializers.RecipeSerializer

        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    # NOTE: perform_create method is called during the POST processing flow in DRF;
    # Runs after data validation and before saving the data to the database.

    # NOTE: This pattern is common in DRF when creating resources that belong to users:
    # doesn't accept a user field from clients, but instead assigns the user field
    # to the authenticated user that made the request.
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
