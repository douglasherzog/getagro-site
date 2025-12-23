from django.contrib import admin

# Register your models here.

from .models import Lead, MessageTemplate


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "interest", "name", "email", "phone")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("interest", "created_at")


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("channel", "title", "is_active", "updated_at")
    list_filter = ("channel", "is_active", "updated_at")
    search_fields = ("title", "subject", "body")
