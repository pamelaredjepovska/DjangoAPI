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


# View for creating company records
class CreateCompanyView(CreateAPIView):
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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


# Custom Pagination Class
class CompanyPagination(PageNumberPagination):
    page_size = 5  # Define how many companies per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Optional: limit the max page size


# View to list all companies owned by the authenticated user
class ListUserCompaniesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
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
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the company object
        company = super().get_object()

        # Ensure the authenticated user is the owner of the company
        if company.owner != self.request.user:
            raise PermissionDenied(
                {"error": "You do not have permission to view this company."}
            )

        return company


# View to update the company record (only number_of_employees)
class UpdateCompanyView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the user can only update their own company
        company = super().get_object()
        if company.owner != self.request.user:
            raise PermissionDenied(
                {"error": "You do not have permission to update this company."}
            )
        return company

    def patch(self, request, *args, **kwargs):
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
