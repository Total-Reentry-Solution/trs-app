# Generated by Django 5.0 on 2024-01-19 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reentry", "0007_alter_question_options_question_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionnaireCategory",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="questionnaire",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reentry.questionnairecategory",
            ),
        ),
    ]
