from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags import views

router = DefaultRouter()
router.register("", views.TagViewSet, basename="tag")

app_name = "tags"

urlpatterns = [
    path("", include(router.urls)),
]
