from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_profile_cpf_per_role"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="profile",
            name="unique_cpf_per_role",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="cpf",
            new_name="document",
        ),
        migrations.AlterField(
            model_name="profile",
            name="document",
            field=models.CharField(max_length=14, unique=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="phone",
            field=models.CharField(blank=True, default="", max_length=40),
            preserve_default=False,
        ),
    ]
