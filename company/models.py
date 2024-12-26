from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    A model representing a company with its details.

    Attributes:
        id (AutoField): The primary key for the company.
        company_name (CharField): The name of the company.
        description (TextField): A detailed description of the company.
        number_of_employees (PositiveIntegerField): The number of employees in the company.
        owner (ForeignKey): A reference to the User model, indicating the owner of the company.
    """

    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    number_of_employees = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")

    def __str__(self):
        """
        Return company name as string representation
        """
        return self.company_name

    # def delete(self, *args, **kwargs):
    #     """
    #     Prevents the deletion of company records through the ORM.
    #     """
    #     raise PermissionDenied("Deleting company records is not allowed.")

    # @classmethod
    # def delete_objects(cls, *args, **kwargs):
    #     """
    #     Prevents the bulk deletion of company records.
    #     """
    #     raise PermissionDenied("Bulk deletion of company records is not allowed.")
