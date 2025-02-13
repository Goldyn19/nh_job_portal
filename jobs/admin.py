from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "employer_id", "category", "is_active", "created_at")
    search_fields = ("title", "category", "employer_id__username")
    list_filter = ("category", "is_active")
