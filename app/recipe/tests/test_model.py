from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from recipe.models import Recipe

# Create your tests here.


class RecipeTests(TestCase):
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        recipe = Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample receipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)
