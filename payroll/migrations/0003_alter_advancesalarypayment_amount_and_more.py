# Generated by Django 5.1.3 on 2024-12-12 16:47

import core.models.fields.datefield
import core.models.fields.floatfield
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0002_remove_payroll_metadata_payroll__metadata_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advancesalarypayment",
            name="amount",
            field=core.models.fields.floatfield.FloatField(verbose_name="montant"),
        ),
        migrations.AlterField(
            model_name="advancesalarypayment",
            name="date",
            field=core.models.fields.datefield.DateField(verbose_name="date"),
        ),
    ]
