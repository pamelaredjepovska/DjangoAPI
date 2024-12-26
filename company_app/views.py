from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A custom view for obtaining a pair of access and refresh tokens.

    This class overrides the default `TokenObtainPairView` to use a custom
    serializer, `CustomTokenObtainPairSerializer`, for token generation.

    Args:
        TokenObtainPairView (class): The parent view class for handling token
                                     pair generation.
    Attributes:
        serializer_class (CustomTokenObtainPairSerializer): The custom serializer
                                                             used to validate
                                                             and create tokens.
    """

    serializer_class = CustomTokenObtainPairSerializer
