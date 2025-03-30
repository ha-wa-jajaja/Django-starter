from django.conf import settings
from django.db import models


# NOTE: In real world example, this could maybe be in the recipe app
# Since there could be multiple tag types for different apps
class Tag(models.Model):
    """Tag for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
