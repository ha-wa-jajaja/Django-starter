from django.conf import settings
from django.db import models


class Menu(models.Model):
    """Menu object."""

    # NOTE: Uses models.TextChoices to define a ENUM like class
    class MenuTypes(models.TextChoices):
        BREAKFAST = "Breakfast"
        LUNCH = "Lunch"
        DINNER = "Dinner"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recipes = models.ManyToManyField("recipe.Recipe")
    type = models.CharField(
        max_length=10, choices=MenuTypes.choices, default=MenuTypes.DINNER
    )

    # NOTE: Properties are built in Python decorator used to define computed attributes
    @property
    def is_empty(self):
        """Check if the menu is empty."""
        return not self.recipes.exists()

    def __str__(self):
        return self.title
