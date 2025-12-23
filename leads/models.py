from django.db import models

# Create your models here.


class Lead(models.Model):
    class Interest(models.TextChoices):
        SELLER = "seller", "Vender gado"
        BUYER = "buyer", "Comprar gado (Frigorífico)"
        OTHER = "other", "Outros assuntos"

    interest = models.CharField(max_length=20, choices=Interest.choices, default=Interest.OTHER)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()

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
