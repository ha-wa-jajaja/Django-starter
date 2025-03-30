from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from tags.models import Tag

# Create your tests here.


class RecipeTests(TestCase):
    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
