# Generated by Django 5.1.3 on 2024-12-27 13:14

import core.models.fields.foreignkey
import core.models.fields.model_select_field
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0006_alter_permission_content_type_alter_permission_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permission",
            name="content_type",
            field=core.models.fields.foreignkey.ForeignKey(
                default=None,
                limit_choices_to={"app_label__in": ["core", "employee", "payroll"]},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="permissions",
                to="contenttypes.contenttype",
                verbose_name="content type",
            ),
        ),
        migrations.AlterField(
            model_name="permission",
            name="user",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="permissions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="rowlevelsecurity",
            name="content_type",
            field=core.models.fields.foreignkey.ForeignKey(
                default=None,
                limit_choices_to={"app_label__in": ["core", "employee", "payroll"]},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rows",
                to="contenttypes.contenttype",
                verbose_name="content type",
            ),
        ),
        migrations.AlterField(
            model_name="rowlevelsecurity",
            name="user",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rows",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]