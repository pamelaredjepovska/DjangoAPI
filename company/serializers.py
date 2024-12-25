from rest_framework import serializers
from .models import Company


# Convert company data model to JSON format
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


# For creating a company with specific fields
class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "description", "number_of_employees"]


# Serializer to handle partial updates
class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        # Only allow the number_of_employees field to be updated
        fields = ["number_of_employees"]
