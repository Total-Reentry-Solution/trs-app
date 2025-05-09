# Generated by Django 5.0 on 2023-12-07 05:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CareTeam",
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
                ("name", models.CharField(max_length=100)),
                ("organization", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Mentor",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("organization", models.CharField(max_length=100)),
                (
                    "care_teams",
                    models.ManyToManyField(
                        blank=True, related_name="mentors", to="reentry.careteam"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParoleOfficer",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("organization", models.CharField(max_length=100)),
                (
                    "care_teams",
                    models.ManyToManyField(
                        blank=True,
                        related_name="parole_officers",
                        to="reentry.careteam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReturningCitizen",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "care_team",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reentry.careteam",
                    ),
                ),
            ],
        ),
    ]
