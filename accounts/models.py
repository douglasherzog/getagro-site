from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    ROLE_BUYER = "buyer"
    ROLE_SELLER = "seller"
    ROLE_BOTH = "both"

    ROLE_CHOICES = [
        (ROLE_BUYER, "Comprador"),
        (ROLE_SELLER, "Vendedor"),
        (ROLE_BOTH, "Comprador e Vendedor"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=160)
    document = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    cep = models.CharField(max_length=8, blank=True, default="")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
