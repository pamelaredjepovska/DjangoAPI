from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.conf import settings

from company.models import Company
from .serializers import CompanyListSerializer
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Test API view used for checking authentication
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})


# View for creating company records
class CreateCompanyView(generics.CreateAPIView):
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

        # Paginate the companies
        paginator = CompanyPagination()
        paginated_companies = paginator.paginate_queryset(companies, request)

        # Serialize the data, send JSON format as a response
        serializer = CompanyListSerializer(paginated_companies, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
