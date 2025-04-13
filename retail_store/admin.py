from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Business, CustomUser, CashierLoginID

# Register Business model
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "address")
    search_fields = ("name", "email", "phone")


# Customizing UserAdmin for CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "business")
    search_fields = ("username", "email", "role")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Business Details", {"fields": ("role", "business")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )


# Register CashierLoginID model
@admin.register(CashierLoginID)
class CashierLoginIDAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "expires_at", "is_used")
    search_fields = ("id", "user__username")
    list_filter = ("is_used",)
