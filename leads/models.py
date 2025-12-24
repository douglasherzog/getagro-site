from django.conf import settings
from django.db import models

from accounts.models import Profile

# Create your models here.


class Lead(models.Model):
    class Source(models.TextChoices):
        LEGACY_FORM = "legacy_form", "Formulário"
        LISTING = "listing", "Interesse em anúncio"
        PROCURA = "procura", "Interesse em procura"

    class Status(models.TextChoices):
        NEW = "new", "Novo"
        IN_PROGRESS = "in_progress", "Em andamento"
        CONTACT_RELEASED = "contact_released", "Contato liberado"
        CLOSED = "closed", "Fechado"
        LOST = "lost", "Perdido"

    class ContactRelease(models.TextChoices):
        NONE = "none", "Não liberar"
        BOTH = "both", "A) Liberar para ambos"
        SELLER_ONLY = "seller_only", "B) Liberar só do vendedor"
        BUYER_ONLY = "buyer_only", "C) Liberar só do comprador"

    class Interest(models.TextChoices):
        SELLER = "seller", "Vender gado"
        BUYER = "buyer", "Comprar gado (Frigorífico)"
        OTHER = "other", "Outros assuntos"

    source = models.CharField(max_length=20, choices=Source.choices, default=Source.LEGACY_FORM)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    listing = models.ForeignKey(
        "listings.Listing",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
    )
    procura = models.ForeignKey(
        "leads.Procura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
    )

    interest = models.CharField(max_length=20, choices=Interest.choices, default=Interest.OTHER)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    contact_release = models.CharField(max_length=20, choices=ContactRelease.choices, default=ContactRelease.NONE)
    contact_released_at = models.DateTimeField(null=True, blank=True)

    city_state = models.CharField(max_length=120, blank=True)
    heads = models.PositiveIntegerField(null=True, blank=True)
    avg_weight_kg = models.PositiveIntegerField(null=True, blank=True)
    animal_category = models.CharField(max_length=80, blank=True)
    breed = models.CharField(max_length=80, blank=True)
    timeframe = models.CharField(max_length=120, blank=True)

    specs = models.TextField(blank=True)
    desired_volume = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class MessageTemplate(models.Model):
    class Channel(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "E-mail"

    channel = models.CharField(max_length=20, choices=Channel.choices)
    title = models.CharField(max_length=160)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["channel", "title"]

    def __str__(self) -> str:
        return f"{self.get_channel_display()}: {self.title}"


class Procura(models.Model):
    buyer_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="procuras")
    title = models.CharField(max_length=160)
    specs = models.TextField(blank=True)
    desired_volume = models.CharField(max_length=120, blank=True)
    city_state = models.CharField(max_length=120, blank=True)
    heads = models.PositiveIntegerField(null=True, blank=True)
    avg_weight_kg = models.PositiveIntegerField(null=True, blank=True)
    animal_category = models.CharField(max_length=80, blank=True)
    breed = models.CharField(max_length=80, blank=True)
    timeframe = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.buyer_profile.document})"
