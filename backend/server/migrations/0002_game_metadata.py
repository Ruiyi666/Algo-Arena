# Generated by Django 4.2.4 on 2023-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="metadata",
            field=models.JSONField(default=dict, verbose_name="Metadata"),
        ),
    ]
