from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra info", {"fields": ("full_name", "contact")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra info", {"fields": ("full_name", "contact")}),
    )
    list_display = ("username", "full_name", "email", "contact", "is_staff")
    search_fields = ("username", "full_name", "email")