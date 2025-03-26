from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    # NOTE: These two lines declares what data AuthTokenSerializer should expect when receives a request.
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""

        email = attrs.get("email")
        password = attrs.get("password")

        # NOTE: authenticate() is to verify a user's credentials
        # And returns the corresponding User object or None(if no user matches)
        user = authenticate(
            # NOTE: self.context is a dictionary that is made available to a serializer's methods
            #  during the serialization/deserialization process.
            # NOTE:Even if a simple username/password check doesn't need the request,
            # including it maintains consistency in how authenticate() is called across different scenarios
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        return {"user": user}

        # NOTE: Course return attrs, but not needed
        # attrs['user'] = user
        # return attrs
