from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the custom User model"""

    # Fields shown in the list view
    list_display = ("email", "username", "phone_number", "is_staff", "is_verified", "is_active")
    list_filter = ("is_staff", "is_verified", "is_active", "is_superuser")
    search_fields = ("email", "username", "phone_number")
    ordering = ("email",)

    # Fieldsets for editing users in the admin
    fieldsets = (
        (None, {"fields": ("email", "username", "phone_number", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_verified", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # Fieldsets when creating a new user in the admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "phone_number", "password1", "password2", "is_staff", "is_verified", "is_active"),
        }),
    )
