import os
import uuid

from django.conf import settings
from django.db import models


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class Recipe(models.Model):
    """Recipe object."""

    user = models.ForeignKey(
        # NOTE: Django automatically assumes foreign keys link to the primary key of the referenced model
        settings.AUTH_USER_MODEL,
        # NOTE: CASCADE: when the referenced foreign key object is deleted,
        # all model objects that refer to that FK are also deleted.
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # NOTE: ManyToManyField auto creates a junction table to link the two models
    tags = models.ManyToManyField(
        # NOTE: Using string reference, we're able to:
        # 1. Avoid circular import issues
        # 2.Allow References to Models Not Yet Defined
        # 3.Enable Cross-App References Without Direct Dependencies
        # 4.Support for Lazy Loading
        "tags.Tag",
    )
    ingredients = models.ManyToManyField("ingredient.Ingredient")
    # NOTE: ImageField is a built-in FileField with additional validation for image files
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
