from django.db.models import Max, Min
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer, ProductsInfoSerializer


@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_info(request):
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
