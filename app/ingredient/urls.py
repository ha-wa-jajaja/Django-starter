from django.urls import include, path
from ingredient import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.IngredientViewSet, basename="ingredient")

app_name = "ingredients"

urlpatterns = [
    path("", include(router.urls)),
]
