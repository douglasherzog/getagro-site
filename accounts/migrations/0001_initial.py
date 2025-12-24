from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("buyer", "Comprador"), ("seller", "Vendedor")], max_length=16)),
                ("full_name", models.CharField(max_length=160)),
                ("cpf", models.CharField(max_length=14, unique=True)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=120)),
                ("state", models.CharField(max_length=2)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
