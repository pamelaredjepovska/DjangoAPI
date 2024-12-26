from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    A serializer to convert the Company data model to JSON format.

    Meta:
        model (Model): The Company model being serialized.
        fields (str): Specifies all fields of the model to be included in the serialized output.
    """

    class Meta:
        model = Company
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    """
    A serializer for creating or retrieving a subset of Company fields.

    Meta:
        model (Model): The Company model being serialized.
        fields (list): Specifies the fields to be included in the serialized output.
    """

    class Meta:
        model = Company
        fields = ["company_name", "description", "number_of_employees"]


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer for handling partial updates to the Company model.

    Meta:
        model (Model): The Company model being serialized.
        fields (list): Specifies the fields that can be updated.
    """

    class Meta:
        model = Company
        # Only allow the number_of_employees field to be updated
        fields = ["number_of_employees"]
