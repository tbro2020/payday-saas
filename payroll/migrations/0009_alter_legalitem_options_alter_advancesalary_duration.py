# Generated by Django 5.0.4 on 2024-06-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0008_rename_addition_items_payroll_additional_items"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="legalitem",
            options={
                "verbose_name": "Retenue légale",
                "verbose_name_plural": "Retenues légales",
            },
        ),
        migrations.AlterField(
            model_name="advancesalary",
            name="duration",
            field=models.IntegerField(
                default=36, help_text="nombre de mois", verbose_name="durée"
            ),
        ),
    ]
