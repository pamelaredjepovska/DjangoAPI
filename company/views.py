from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView

from django.conf import settings

from company.models import Company
from .serializers import CompanyListSerializer, CompanyUpdateSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Test API view used for checking authentication
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})


class CreateCompanyView(CreateAPIView):
    """
    A view for creating a new company with user-specific constraints and sending a notification.

    Attributes:
        serializer_class (CompanyListSerializer): The serializer used for company creation.
        permission_classes (list): Permissions required to access this view,
                                   restricted to authenticated users.

    Methods:
        post(request, *args, **kwargs): Handles the POST request for creating a company,
                                        validating content type and request data.
        perform_create(serializer): Custom logic to limit the number of companies a user can create
                                    and send email notifications upon successful creation.

    Raises:
        ValidationError: If the user has already created the maximum allowed number of companies
                         (5) or if any validation errors occur.
    """

    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Validates the request's content type and body before delegating to the parent method.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: An HTTP response indicating success or failure.
        """

        # Check if the Content-Type is application/json
        if "application/json" not in request.content_type:
            return Response(
                {"error": "Invalid content type. Please provide a JSON object."},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        # Check if the request data is empty
        if not request.data:
            return Response(
                {"error": "Request body is empty. Please provide the required data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Performs additional checks and actions during the company creation process.

        Args:
            serializer (Serializer): The serializer instance containing validated data.

        Raises:
            ValidationError: If the user exceeds the limit of 5 companies.
        """

        user = self.request.user

        # Check if the user has already created 5 companies
        if user.companies.count() >= 5:
            raise ValidationError({"error": "You can only create up to 5 companies."})

        # Save the company with the current user as the owner
        company = serializer.save(owner=user)

        # Render HTML template for the message
        message = render_to_string(
            "confirmation_email.html",
            {"user": user, "company": company},
        )

        # Send email notification
        send_mail(
            subject="New Company Created",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email] if user.email else [settings.DEFAULT_TO_EMAIL],
            html_message=message,
        )


class CompanyPagination(PageNumberPagination):
    """
    Custom pagination class for paginating company listings.

    Attributes:
        page_size (int): The default number of companies per page.
        page_size_query_param (str): The query parameter for the client to set the page size.
        max_page_size (int): The maximum allowable page size to prevent excessive data retrieval.
    """

    page_size = 5  # Define how many companies per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Optional: limit the max page size


class ListUserCompaniesView(APIView):
    """
    A view for listing all companies owned by the authenticated user with optional ordering and pagination.

    Attributes:
        permission_classes (list): Permissions required to access this view,
                                   restricted to authenticated users.

    Methods:
        get(request, *args, **kwargs): Retrieves the list of companies owned by the user,
                                       supports ordering, and returns a paginated response.

    Raises:
        ValidationError: If an invalid ordering field is provided.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to retrieve companies owned by the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Raises:
            ValidationError: If the ordering field is invalid.

        Returns:
            Response: A paginated response containing the serialized company data.
        """

        # Get all companies owned by the authenticated user
        user = request.user
        companies = Company.objects.filter(owner=user)

        # Get ordering parameter from the request
        ordering = request.query_params.get("ordering", None)

        # If an ordering parameter is provided, validate and apply it
        if ordering:
            # Ensure that only valid fields are used for ordering
            valid_ordering_fields = [
                "company_name",
                "description",
                "number_of_employees",
            ]
            if ordering.lstrip("-") not in valid_ordering_fields:
                raise ValidationError(
                    {
                        "error": f"Invalid ordering field. Valid fields are: {', '.join(valid_ordering_fields)}."
                    }
                )

            # Apply ordering
            companies = companies.order_by(ordering)

        # Paginate the companies
        paginator = CompanyPagination()
        paginated_companies = paginator.paginate_queryset(companies, request)

        # Serialize the data, send JSON format as a response
        serializer = CompanyListSerializer(paginated_companies, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class RetrieveUserCompanyView(RetrieveAPIView):
    """
    A view for retrieving a specific company owned by the authenticated user.

    Attributes:
        queryset (QuerySet): The base queryset to retrieve company objects.
        serializer_class (CompanyListSerializer): The serializer used for retrieving company details.
        permission_classes (list): Permissions required to access this view,
                                   restricted to authenticated users.

    Methods:
        get_object(): Retrieves the company object and ensures the authenticated user is its owner.

    Raises:
        PermissionDenied: If the authenticated user is not the owner of the company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the specific company object and validates ownership.

        Raises:
            PermissionDenied: If the authenticated user does not own the company.

        Returns:
            Company: The company object owned by the authenticated user.
        """

        # Retrieve the company object
        company = super().get_object()

        # Ensure the authenticated user is the owner of the company
        if company.owner != self.request.user:
            raise PermissionDenied(
                {"error": "You do not have permission to view this company."}
            )

        return company


class UpdateCompanyView(UpdateAPIView):
    """
    A view for updating the number of employees in a company record.

    Attributes:
        queryset (QuerySet): The base queryset to retrieve company objects.
        serializer_class (CompanyUpdateSerializer): The serializer used for updating company details.
        permission_classes (list): Permissions required to access this view,
                                   restricted to authenticated users.

    Methods:
        get_object(): Ensures the authenticated user is the owner of the company.
        patch(request, *args, **kwargs): Handles the PATCH request to update the company
                                         while enforcing validation rules.

    Raises:
        PermissionDenied: If the authenticated user is not the owner of the company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the specific company object and validates ownership.

        Raises:
            PermissionDenied: If the authenticated user does not own the company.

        Returns:
            Company: The company object owned by the authenticated user.
        """

        # Ensure the user can only update their own company
        company = super().get_object()
        if company.owner != self.request.user:
            raise PermissionDenied(
                {"error": "You do not have permission to update this company."}
            )

        return company

    def patch(self, request, *args, **kwargs):
        """
        Handles the PATCH request to update the company's 'number_of_employees' field.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The response indicating the success or failure of the update.

        Raises:
            Response: If the request body is empty or contains invalid fields.
        """

        # First, check permissions by calling `get_object`
        self.get_object()

        # Validate if the request has a JSON body
        if not request.data:
            return Response(
                {"error": "Request body is empty. Please provide valid data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate if the request contains only the allowed field 'number_of_employees'
        if set(request.data.keys()) != {"number_of_employees"}:
            return Response(
                {"error": "Only 'number_of_employees' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Perform partial update on the database relation
        return super().patch(request, *args, **kwargs)
