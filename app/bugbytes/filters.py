import django_filters
from .models import Product
from rest_framework import filters

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # NOTE: We can use django_filters to apply filters
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range']
        }