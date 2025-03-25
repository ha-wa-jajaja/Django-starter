"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (UserSerializer, AuthTokenSerializer)

# NOTE: generics.CreateAPIView is Django REST Framework specified POST request handler.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # NOTE: serializer_class is a built-in attribute in Django REST Framework that specifies serializer for the view
    # 1. When a POST request arrives, CreateAPIView looks at the serializer_class
    # 2. Then it creates an instance of the UserSerializer and passes the request data to it.
    # 3. The serializer validates the data using definition from UserSerializer.Meta
    # 4. After validation, CreateAPIView calls serializer's save() method, which in turn calls the serializer's create() method
    # 5. Finally, the view returns an appropriate response
    serializer_class = UserSerializer

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
