# Generated by Django 4.2 on 2024-10-08 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("provider", "0001_initial"),
        ("exchange", "0003_currencyexchangerate_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="currencyexchangerate",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="currencyexchangerate",
            name="priority",
        ),
        migrations.AlterField(
            model_name="currencyexchangerate",
            name="provider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="provider.provider"
            ),
        ),
    ]
