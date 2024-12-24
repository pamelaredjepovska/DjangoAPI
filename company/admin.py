from django.contrib import admin
from .models import Company


# Register company model
class CompanyAdmin(admin.ModelAdmin):
    # Columns displayed in the admin list view
    list_display = ("company_name", "owner", "number_of_employees")
    # Enables searching for companies by these fields
    search_fields = ("company_name", "owner__username")
    list_filter = ("owner",)


admin.site.register(Company, CompanyAdmin)
