# Generated by Django 5.1.5 on 2025-01-20 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clashroyale", "0004_alter_battlelog_options_alter_gamemode_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Leaderboard",
        ),
    ]
