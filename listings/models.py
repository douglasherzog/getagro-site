from django.db import models

from accounts.models import Profile


class Listing(models.Model):
    class ListingType(models.TextChoices):
        LOT = "lot", "Lote"
        ANIMAL = "animal", "Animal"

    seller_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="listings")

    listing_type = models.CharField(max_length=10, choices=ListingType.choices)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)

    heads = models.PositiveIntegerField(null=True, blank=True)
    avg_weight_kg = models.PositiveIntegerField(null=True, blank=True)
    animal_category = models.CharField(max_length=80, blank=True)
    breed = models.CharField(max_length=80, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_listing_type_display()}: {self.title}"
