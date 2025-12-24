from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cpf",
            field=models.CharField(max_length=14),
        ),
        migrations.AddConstraint(
            model_name="profile",
            constraint=models.UniqueConstraint(fields=("cpf", "role"), name="unique_cpf_per_role"),
        ),
    ]
