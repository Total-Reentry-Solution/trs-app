# Generated by Django 5.0 on 2024-01-22 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reentry", "0009_userresponse_submitted_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="userresponse",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="userresponse",
            name="updated",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
