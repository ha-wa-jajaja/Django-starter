"""
Serializers for recipe APIs
"""

from typing import List

from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer
from recipe.models import Recipe
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    # Instead of a custom field, use a PrimaryKeyRelatedField with many=True
    # This will ensure Swagger properly shows it as a list of integers
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all(), required=False
    )

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags", "ingredients"]
        read_only_fields = ["id"]

    # NOTE: validate_<field_name> is a built-in field-level validation system in DRF.
    def validate_tags(self, tags):
        """Validate that tags belong to the user."""
        user = self.context["request"].user
        for tag in tags:
            if tag.user != user:
                raise serializers.ValidationError(
                    f"Tag with id {tag.id} does not belong to this user"
                )
        return tags

    def validate_ingredients(self, ingredients):
        """Validate that ingredients belong to the user."""
        user = self.context["request"].user
        for ingredient in ingredients:
            if ingredient.user != user:
                raise serializers.ValidationError(
                    f"Ingredient with id {ingredient.id} does not belong to this user"
                )
        return ingredients

    def to_representation(self, instance):
        """Convert the representation to include full tag data."""
        ret = super().to_representation(instance)
        ret["tags"] = TagSerializer(instance.tags.all(), many=True).data
        ret["ingredients"] = IngredientSerializer(
            instance.ingredients.all(), many=True
        ).data
        return ret


# NOTE: "serializer optimization pattern" in Django REST Framework:
# Only include data needed for the current request in serializer responses.
# In this case, Only when getting the detail view, the description field is needed in the response.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
