from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    number_of_employees = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")

    def __str__(self):
        return self.company_name

    # Prevent record deletion through ORM
    # def delete(self, *args, **kwargs):
    #     raise PermissionDenied("Deleting company records is not allowed.")

    # @classmethod
    # def delete_objects(cls, *args, **kwargs):
    #     raise PermissionDenied("Bulk deletion of company records is not allowed.")
