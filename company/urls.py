from django.urls import path
from .views import (
    ListUserCompaniesView,
    ProtectedView,
    CreateCompanyView,
    UpdateCompanyView,
)

urlpatterns = [
    # A protected test route that requires authentication
    path("api/protected/", ProtectedView.as_view(), name="protected_view"),
    # A route that allows the user to create a company record
    path("create/", CreateCompanyView.as_view(), name="create_company"),
    # A route that fetches all company records created by the current user
    path("", ListUserCompaniesView.as_view(), name="list_user_companies"),
    # A route that updates a company's record's number of employees
    path("<int:pk>/update/", UpdateCompanyView.as_view(), name="update_company"),
]
