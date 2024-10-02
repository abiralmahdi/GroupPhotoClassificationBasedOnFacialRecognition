from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Extend the default UserAdmin to handle the custom fields in your User model
class CustomUserAdmin(UserAdmin):
    # Define which fields to display in the admin panel
    list_display = ('username', 'email', 'first_name', 'last_name', 'contact', 'is_staff')
    # Add fieldsets for creating and editing users
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact', 'profilepicture')}),
    )

# Register the custom User model
admin.site.register(User, CustomUserAdmin)
