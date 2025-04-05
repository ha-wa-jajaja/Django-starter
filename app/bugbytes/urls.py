from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views


router = DefaultRouter()
router.register('orders', views.OrderViewSet)

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view()),
    path("products/info/", views.ProductsInfoAPIView.as_view()),
    path("products/<int:pk>/", views.product_detail),
    path("product-view/<int:product_id>", views.ProductDetailAPIView.as_view()),
    path("user-orders/", views.UserOrderListAPIView.as_view()),
]

urlpatterns += router.urls

