from django.contrib import admin
from .models import Company


# Register company model
class CompanyAdmin(admin.ModelAdmin):
    # Columns displayed in the admin list view
    list_display = ("company_name", "owner", "number_of_employees")
    # Enables searching for companies by these fields
    search_fields = ("company_name", "owner__username")
    list_filter = ("owner",)

    # # Disable the delete permission for all users
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # # Remove the bulk "delete selected" action in admin
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if "delete_selected" in actions:
    #         del actions["delete_selected"]
    #     return actions


admin.site.register(Company, CompanyAdmin)
