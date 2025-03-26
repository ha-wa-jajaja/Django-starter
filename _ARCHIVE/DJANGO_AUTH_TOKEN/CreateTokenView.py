from AuthTokenSerializer import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# NOTE: ObtainAuthToken is a built-in view in Django REST Framework
# That accepts POST requests to allow users to obtain an authentication token by submitting their username and password.
# DOC: https://www.django-rest-framework.org/api-guide/authentication/
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    # NOTE: post() of ObtainAuthToken runs serializer.is_valid(), and it runs validate() inside
    serializer_class = AuthTokenSerializer

    # NOTE: This is a setting within DRF that specifies the default renderer classes that DRF should use
    # if not otherwise specified in a view. By default, it usually includes JSONRenderer.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# USAGE
# path("token/", views.CreateTokenView.as_view(), name="token"),
