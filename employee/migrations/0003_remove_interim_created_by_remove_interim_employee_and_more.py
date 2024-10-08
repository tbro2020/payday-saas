# Generated by Django 5.0.4 on 2024-09-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0002_position_working_days_per_month"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="is_housed",
            field=models.BooleanField(default=False, verbose_name="logé"),
        ),
        migrations.AddField(
            model_name="employee",
            name="mileage_allowance",
            field=models.BooleanField(default=0, verbose_name="indemnité kilométrique"),
        )
    ]
