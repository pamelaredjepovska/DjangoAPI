from django.urls import path
from .views import ProtectedView, CreateCompanyView

urlpatterns = [
    # A protected test route that requires authentication
    path("api/protected/", ProtectedView.as_view(), name="protected_view"),
    # A route that allows the user to create a company record
    path("create/", CreateCompanyView.as_view(), name="create_company"),
]
