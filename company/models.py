from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    number_of_employees = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")

    def __str__(self):
        return self.company_name
