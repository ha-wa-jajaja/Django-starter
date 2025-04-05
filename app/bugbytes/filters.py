import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # NOTE: We can use django_filters to apply filters
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range']
        }