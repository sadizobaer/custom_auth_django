# Generated by Django 4.2.4 on 2023-12-20 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("id_name", models.CharField(max_length=50, unique=True)),
                ("phonenumber", models.CharField(blank=True, max_length=15, null=True)),
                ("password", models.CharField(max_length=128)),
            ],
        ),
    ]
