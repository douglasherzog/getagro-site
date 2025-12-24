from django.contrib import admin

from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("created_at", "listing_type", "title", "seller_profile")
    list_filter = ("listing_type", "created_at")
    search_fields = ("title", "description", "seller_profile__full_name", "seller_profile__cpf")
