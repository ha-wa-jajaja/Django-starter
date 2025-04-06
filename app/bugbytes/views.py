from django.db.models import Max, Min
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import InStockFilterBackend, OrderFilter, ProductFilter
from .models import Order, Product
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    ProductSerializer,
    ProductsInfoSerializer,
)


# NOTE: DRF provides set of custom generic views to handle common tasks
# In this case, ListCreateAPIView to handle both listing and creating products
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    # NOTE: Allowing to request a specific number of records (limit) starting from a
    # particular position (offset) in the result set.
    # pagination_class = LimitOffsetPagination

    # NOTE: PageNumberPagination is the standard pagination we're used to
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'page'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 4

    filter_backends = [
        # Note: Must also add this to ensure proper doc, even already applied ProductSerializer
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        # NOTE: This will be directly applied
        InStockFilterBackend,
    ]
    search_fields = ["=name", "description"]
    ordering_fields = ["name", "price", "stock"]

    # NOTE: CACHING: 60 * 15 is 15 minutes
    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # NOTE: This method is for demo purpose: to show the cache actually works
    def get_queryset(self):
        import time

        time.sleep(2)
        return super().get_queryset()

    # NOTE: Customize the permission classes for this view
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        # This line triggers the parents get_permissions() method
        # to apply the permission classes from its descendants
        return super().get_permissions()


# NOTE: Django also allows to use function-based views
@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


# NOTE:
# APIView is a class-based view provided by Django REST framework
# Allows more flexibility and customization compared to function-based views
# It provides methods like get(), post(), put(), delete() to handle different HTTP methods
# It also provides access to request and response objects,
# making it easier to work with API requests and responses
class ProductsInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductsInfoSerializer(
            {
                "products": products,
                "count": len(products),
                # NOTE:
                # .aggregate() is a Django QuerySet method that performs a calculation over all objects and returns a dictionary
                # max_price=Max('price') is specifying what we want to calculate
                # ['max_price'] is accessing the result of the aggregation by its key
                # aggregate() transforms to a SQL command to calculate in DB level, making it more efficient
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
                "min_price": products.aggregate(min_price=Min("price"))["min_price"],
            }
        )
        return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # NOTE:
    # By default, Django uses:
    # lookup_field = 'pk' -> The field to use for lookups
    # lookup_url_kwarg = 'pk' -> The URL parameter name to use for the lookup
    # In this case, we are overriding the default behavior to use 'product_id' instead of 'pk'
    # This lookup is used to retrieve the object from the database
    # Ensure only one item is returned
    lookup_url_kwarg = "product_id"


class UserOrderListAPIView(generics.ListAPIView):
    # NOTE:
    # prefetch_related() is used to optimize database access by reducing the number of queries
    # especially when dealing with many-to-many relationships
    # Detail: notes/django/prefetch_related.md
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
