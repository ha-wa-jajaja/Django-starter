from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("products/info/", views.product_info),
    path("products/<int:pk>/", views.product_detail),
    path("product-view/<int:product_id>", views.ProductDetailAPIView.as_view()),
    path("orders/", views.order_list),
    path("user-orders/", views.UserOrderListAPIView.as_view()),
]
