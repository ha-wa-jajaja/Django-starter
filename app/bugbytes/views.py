from django.db.models import Max, Min
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer, ProductsInfoSerializer


# NOTE: DRF provides set of custom generic views to handle common tasks
# In this case, ListCreateAPIView to handle both listing and creating products
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # NOTE: Customize the permission classes for this view
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        # This line triggers the parents get_permissions() method
        # to apply the permission classes from its descendants
        return super().get_permissions()


@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# NOTE: Django also allows to use function-based views
@api_view(["GET"])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


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
