from django.conf import settings
from django.db import models


class Menu(models.Model):
    """Menu object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recipes = models.ManyToManyField("recipe.Recipe")

    def __str__(self):
        return self.title
