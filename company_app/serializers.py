from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Get the data from the request body
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        # Try to find user by email first
        user = None
        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        if not user:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                user = None

        # If no user found
        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        # Check password
        if user and not user.check_password(password):
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the tokens in the response
        return {
            "access": access_token,
            "refresh": str(refresh),
        }
