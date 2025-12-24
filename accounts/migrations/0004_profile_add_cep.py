from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_profile_document_email_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="cep",
            field=models.CharField(blank=True, default="", max_length=8),
        ),
    ]
