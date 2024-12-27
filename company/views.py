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
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django.core.mail import send_mail
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateCompanyView(CreateAPIView):
    """
    A view for creating a new company, validating content, and notifying the user via email.

    Attributes:
        serializer_class (CompanyListSerializer): Serializer for company creation.
        permission_classes (list): Permissions to access the view (authenticated users only).
    """

    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="A view for creating a new company, validating content, and notifying the user via email.",
        request_body=CompanyListSerializer,
        responses={
            201: "Company created successfully.",
            400: "Validation error or request issues.",
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Validate the request before processing it.

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
            serializer (Serializer): The validated serializer data.

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
        try:
            send_mail(
                subject="New Company Created",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=(
                    [user.email] if user.email else [settings.DEFAULT_TO_EMAIL]
                ),
                html_message=message,
            )
        except Exception as e:
            raise ValidationError({"error": f"Failed to send email: {str(e)}"})


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
    A view for listing all companies owned by the authenticated user with pagination and optional ordering.

    Attributes:
        permission_classes (list): Permissions to access the view (authenticated users only).
    """

    permission_classes = [IsAuthenticated]

    # Define parameters for Swagger (APIView doesn't expose them)
    @swagger_auto_schema(
        operation_description="A view for listing all companies owned by the authenticated user with pagination and optional ordering.",
        manual_parameters=[
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                description="Number of results per page.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                description="Field to order by (e.g., 'company_name', '-company_name').",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: "Paginated list of companies.",
            400: "Invalid ordering field or request issues.",
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieves the list of companies, supports sorting and pagination.

        Args:
            request (Request): The HTTP request object.

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
    A view to retrieve a specific company record owned by the authenticated user.

    Attributes:
        serializer_class (CompanyListSerializer): Serializer used for retrieving company details.
        permission_classes (list): Permissions to access the view (authenticated users only).
    """

    queryset = Company.objects.none()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="A view to retrieve a specific company record owned by the authenticated user.",
        responses={
            200: "Company details retrieved successfully.",
            404: "We couldn’t find the company, or it’s not associated with your account.",
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve the company record owned by the user.
        """
        try:
            company = Company.objects.get(id=self.kwargs["pk"], owner=request.user)
        except Company.DoesNotExist:
            raise NotFound(
                {
                    "error": "We couldn’t find the company, or it’s not associated with your account."
                }
            )

        # If company is found and belongs to the user, return the response
        serializer = self.get_serializer(company)

        return Response(serializer.data)


class UpdateCompanyView(UpdateAPIView):
    """
    A view for updating the number of employees in a company record.

    Attributes:
        serializer_class (CompanyUpdateSerializer): The serializer used for partial updates.
        permission_classes (list): Permissions to access the view (authenticated users only).
    """

    queryset = Company.objects.none()
    serializer_class = CompanyUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]  # Allow only PATCH method

    def get_object(self):
        """
        Retrieves the specific company object and validates ownership.

        Raises:
            PermissionDenied: If the authenticated user does not own the company.
            NotFound: If the company record does not exist.

        Returns:
            Company: The company object owned by the authenticated user.
        """

        # Try to fetch company by ID
        try:
            company = Company.objects.get(id=self.kwargs["pk"])
        except Company.DoesNotExist:
            raise NotFound({"error": "Company not found."})

        # Ensure the user can only update their own company
        if company.owner != self.request.user:
            raise PermissionDenied(
                {"error": "You do not have permission to update this company."}
            )

        return company

    @swagger_auto_schema(
        operation_description="Partially update the number of employees in a company record.",
        request_body=CompanyUpdateSerializer,
        responses={
            200: "Company updated successfully.",
            400: "Invalid request body or data.",
            403: "Permission denied.",
            404: "Company not found.",
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Handles the PATCH request to update the company's employee count.

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
        if "number_of_employees" not in request.data:
            return Response(
                {"error": "Only 'number_of_employees' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Perform partial update on the database relation
        super().patch(request, *args, **kwargs)

        # Return success message
        return Response(
            {
                "message": "Company updated successfully.",
            },
            status=status.HTTP_200_OK,
        )
