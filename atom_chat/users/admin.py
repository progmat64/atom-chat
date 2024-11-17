from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_moderator",
        "is_blocked",
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_moderator", "is_blocked")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("is_moderator", "is_blocked")}),
    )
