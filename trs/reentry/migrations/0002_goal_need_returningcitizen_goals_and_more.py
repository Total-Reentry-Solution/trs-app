# Generated by Django 5.0 on 2024-01-08 20:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reentry", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Goal",
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
                ("goal", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Need",
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
                ("need", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="returningcitizen",
            name="goals",
            field=models.ManyToManyField(blank=True, to="reentry.goal"),
        ),
        migrations.AddField(
            model_name="returningcitizen",
            name="needs",
            field=models.ManyToManyField(blank=True, to="reentry.need"),
        ),
    ]
