from django.urls import path
from .views import ProtectedView  # Import the view you want to protect

urlpatterns = [
    # A protected test route that requires authentication
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
]