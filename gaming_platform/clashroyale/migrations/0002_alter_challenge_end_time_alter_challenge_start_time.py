# Generated by Django 5.1.5 on 2025-01-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clashroyale", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="challenge",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
