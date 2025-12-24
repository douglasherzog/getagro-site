from django.contrib import admin

# Register your models here.

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "document", "role", "cep", "city", "state")
    search_fields = ("user__username", "full_name", "document", "email", "phone", "cep", "city")
    list_filter = ("role",)
