# Generated by Django 5.0.4 on 2024-06-02 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0004_remove_payslip__employee_alter_payslip_employee"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payslip",
            old_name="employee",
            new_name="_employee",
        ),
    ]
