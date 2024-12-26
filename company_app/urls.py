from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    # Admin interface documentation
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # Admin
    path("admin/", admin.site.urls),
    # Token obtain route for getting access and refresh tokens
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Token refresh route to obtain a new access token using the refresh token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Include the company app urls.py here
    path("api/company/", include("company.urls")),
]
