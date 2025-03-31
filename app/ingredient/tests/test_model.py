from django.contrib.auth import get_user_model
from django.test import TestCase
from ingredient.models import Ingredient


class RecipeTests(TestCase):
    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        ingredient = Ingredient.objects.create(user=user, name="Ingredient1")

        self.assertEqual(str(ingredient), ingredient.name)
