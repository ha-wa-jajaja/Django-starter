
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, OrderSerializer, ProductsInfoSerializer
from .models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max, Min


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductsInfoSerializer({
        'products': products,
        'count': len(products),
        # NOTE:
        # .aggregate() is a Django QuerySet method that performs a calculation over all objects and returns a dictionary
        # max_price=Max('price') is specifying what we want to calculate
        # ['max_price'] is accessing the result of the aggregation by its key
        # aggregate() transforms to a SQL command to calculate in DB level, making it more efficient 
        'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        'min_price': products.aggregate(min_price=Min('price'))['min_price']
    })
    return Response(serializer.data)