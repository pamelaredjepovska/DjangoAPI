from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Token obtain route for getting access and refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token refresh route to obtain a new access token using the refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include the company app urls.py here
    path('', include('company.urls'))
]
