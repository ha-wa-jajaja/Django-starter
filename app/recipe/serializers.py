"""
Serializers for recipe APIs
"""

from recipe.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link"]
        read_only_fields = ["id"]


# NOTE: "serializer optimization pattern" in Django REST Framework:
# Only include data needed for the current request in serializer responses.
# In this case, Only when getting the detail view, the description field is needed in the response.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
