from django.contrib import admin
from .models import Company, Job, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'duration', 'company', 'created_at']
    search_fields = ['title', 'company__name', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['student__username', 'job__title']
    readonly_fields = ['applied_at']