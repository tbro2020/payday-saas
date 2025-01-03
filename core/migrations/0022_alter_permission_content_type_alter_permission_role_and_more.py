# Generated by Django 5.1.3 on 2025-01-03 11:52

import core.models.fields.foreignkey
import core.models.fields.model_select_field
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0021_alter_historicaltemplate_options_and_more"),
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
                verbose_name="type de contenu",
            ),
        ),
        migrations.AlterField(
            model_name="permission",
            name="role",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="permissions",
                to="core.role",
                verbose_name="rôle",
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
                verbose_name="utilisateur",
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
                verbose_name="type de contenu",
            ),
        ),
        migrations.AlterField(
            model_name="rowlevelsecurity",
            name="role",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rows",
                to="core.role",
                verbose_name="rôle",
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
                verbose_name="utilisateur",
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="content_type",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
                verbose_name="type de contenu",
            ),
        ),
    ]
