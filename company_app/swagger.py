from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define Swagger schema view (metadata, access, etc.)
schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version="v1",
        description="API endpoints for Django REST API",
        contact=openapi.Contact(email="pamelaredjepovska@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
