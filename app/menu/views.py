from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Menu
from .serializers import MenuSerializers


# Create your views here.
@api_view(["GET"])
def menu_list(request):
    """View to list all menus."""
    menus = Menu.objects.all()
    serializer = MenuSerializers(menus, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def menu_detail(request, pk):
    """View to retrieve a menu by ID."""
    menu = get_object_or_404(Menu, pk=pk)
    serializer = MenuSerializers(menu)
    return Response(serializer.data)
