from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer
from recipe.models import Recipe
from rest_framework import serializers

from .models import Menu


class MenuSerializers(serializers.ModelSerializer):
    """Serializer for menu objects."""

    recipes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Recipe.objects.all(), required=False
    )
    # NOTE: SerializerMethodField is used to retrieve some computed value
    is_empty = serializers.SerializerMethodField()

    def get_is_empty(self, obj):
        """Get the number of recipes in the menu."""
        return obj.is_empty

    class Meta:
        model = Menu
        fields = ["id", "title", "description", "recipes", "is_empty"]
        read_only_fields = ["id"]

    def validate_title(self, title):
        """Validate if the title is unique."""
        user = self.context["request"].user
        if Menu.objects.filter(title=title, user=user).exists():
            raise serializers.ValidationError(
                f"Recipe with title {title} already exists for this user"
            )
        return title

    # def to_representation(self, instance):
    #     """Convert the representation to include full tag data."""
    #     ret = super().to_representation(instance)
    #     ret["recipes"] = IngredientSerializer(
    #         instance.recipes.all(), many=True
    #     ).data
    #     return ret
