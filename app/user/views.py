"""
Views for the user API.
"""
from rest_framework import generics

from user.serializers import UserSerializer

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
