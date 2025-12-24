from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    ROLE_BUYER = "buyer"
    ROLE_SELLER = "seller"

    ROLE_CHOICES = [
        (ROLE_BUYER, "Comprador"),
        (ROLE_SELLER, "Vendedor"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=160)
    cpf = models.CharField(max_length=14)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cpf", "role"], name="unique_cpf_per_role"),
        ]

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
