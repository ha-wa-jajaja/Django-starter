"""
Serializers for recipe APIs
"""

from typing import List

from recipe.models import Recipe
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer


class RecipeTagField(serializers.Field):
    """Custom field for tags that accepts IDs for write and returns nested data for read."""

    # NOTE: The built-in to_internal_value handles deserialization
    # (converting input data to Python objects)
    def to_internal_value(self, data: List[int]) -> List[Tag]:
        """Accept a list of IDs and convert to tag objects."""
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tag IDs")

        # Get the user from the context
        request = self.context.get("request")
        user = request.user if request else None

        # Validate all tag IDs exist and belong to the user
        tag_objects = []
        for tag_id in data:
            try:
                tag = Tag.objects.get(id=tag_id, user=user)
                tag_objects.append(tag)
            except Tag.DoesNotExist:
                # NOTE: ValidationError defaults to a 400
                # However, 404 could also be valid
                raise serializers.ValidationError(f"Tag with id {tag_id} not found")

        return tag_objects

    # NOTE: The built-in to_representation handles serialization
    # (converting Python objects to output data)
    def to_representation(self, value):
        """Convert tags to full serialized representation."""
        return TagSerializer(value.all(), many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    tags = RecipeTagField(required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]


# NOTE: "serializer optimization pattern" in Django REST Framework:
# Only include data needed for the current request in serializer responses.
# In this case, Only when getting the detail view, the description field is needed in the response.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
