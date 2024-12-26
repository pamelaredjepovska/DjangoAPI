from django.urls import path
from .views import (
    ListUserCompaniesView,
    CreateCompanyView,
    RetrieveUserCompanyView,
    UpdateCompanyView,
)

urlpatterns = [
    # A route that allows the user to create a company record
    path("create/", CreateCompanyView.as_view(), name="create_company"),
    # A route that fetches all company records created by the current user
    path("", ListUserCompaniesView.as_view(), name="list_user_companies"),
    # A route that fetches a company record by its ID
    path(
        "<int:pk>/",
        RetrieveUserCompanyView.as_view(),
        name="retrieve_user_company",
    ),
    # A route that updates a company's record's number of employees
    path("<int:pk>/update/", UpdateCompanyView.as_view(), name="update_company"),
]
