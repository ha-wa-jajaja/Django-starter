from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("", views.menu_list, name="menu-list"),
    path("<int:pk>/", views.menu_detail, name="menu-detail"),
]
