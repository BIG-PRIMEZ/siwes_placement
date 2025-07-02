from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'institution', 'is_staff']
    list_filter = ['user_type', 'institution', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'institution', 'course_of_study', 
                      'year_of_study', 'profile_picture')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)