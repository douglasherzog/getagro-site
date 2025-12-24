from django.contrib import admin

# Register your models here.

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "cpf", "role", "city", "state")
    search_fields = ("user__username", "full_name", "cpf", "city")
    list_filter = ("role",)
