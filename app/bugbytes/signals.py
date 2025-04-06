from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product


# Signals are Django's built-in way of allowing certain senders to notify a set of receivers when certain actions occur.
# Signals intro: https://www.youtube.com/watch?v=8p4M-7VXhAU
@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate product list caches when a product is created, updated, or deleted
    """
    print("Clearing product cache")

    # Clear product list caches
    cache.delete_pattern("*product_list*")
