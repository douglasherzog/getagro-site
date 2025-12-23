from django.contrib import admin

# Register your models here.

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "interest", "name", "email", "phone")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("interest", "created_at")
