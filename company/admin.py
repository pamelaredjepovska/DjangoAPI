from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Company model in the Django admin interface.

    Attributes:
        list_display (tuple): Specifies the columns to display in the admin list view.
        search_fields (tuple): Defines which fields are searchable in the admin interface.
        list_filter (tuple): Allows filtering of companies by owner in the admin list view.
    """

    list_display = ("company_name", "owner", "number_of_employees")
    search_fields = ("company_name", "owner__username")
    list_filter = ("owner",)

    # def has_delete_permission(self, request, obj=None):
    #     """
    #     Prevents deletion of company records in the admin interface.
    #     """
    #     return False

    # def get_actions(self, request):
    #     """
    #     Removes the bulk "delete selected" action in the admin interface.
    #     """
    #     actions = super().get_actions(request)
    #     if "delete_selected" in actions:
    #         del actions["delete_selected"]
    #     return actions


admin.site.register(Company, CompanyAdmin)
