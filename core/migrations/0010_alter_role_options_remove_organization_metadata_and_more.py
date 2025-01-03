# Generated by Django 5.1.3 on 2024-12-27 14:13

import core.models.fields.ace_field
import core.models.fields.booleanfield
import core.models.fields.charfield
import core.models.fields.foreignkey
import core.models.fields.model_select_field
import core.models.fields.model_select_to_multiple_field
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0009_rowlevelsecurity_role_alter_permission_content_type_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="role",
            options={"verbose_name": "rôle", "verbose_name_plural": "rôles"},
        ),
        migrations.RemoveField(
            model_name="organization",
            name="metadata",
        ),
        migrations.AddField(
            model_name="permission",
            name="_import",
            field=core.models.fields.booleanfield.BooleanField(
                default=False, verbose_name="importation"
            ),
        ),
        migrations.AddField(
            model_name="permission",
            name="export",
            field=core.models.fields.booleanfield.BooleanField(
                default=False, verbose_name="exportation"
            ),
        ),
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
            name="create",
            field=core.models.fields.booleanfield.BooleanField(
                default=False, verbose_name="création"
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
            name="update",
            field=core.models.fields.booleanfield.BooleanField(
                default=False, verbose_name="modification"
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
            model_name="role",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=255, unique=True, verbose_name="name"
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
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="roles",
            field=core.models.fields.model_select_to_multiple_field.ModelSelect2Multiple(
                blank=True, to="core.role", verbose_name="rôles"
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="active",
            field=models.BooleanField(
                default=True, help_text="show widget", verbose_name="actif"
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="column",
            field=models.CharField(
                choices=[
                    ("col-md-1 col-xs-12", "1/12"),
                    ("col-md-2 col-xs-12", "2/12"),
                    ("col-md-3 col-xs-12", "3/12"),
                    ("col-md-4 col-xs-12", "4/12"),
                    ("col-md-5 col-xs-12", "5/12"),
                    ("col-md-6 col-xs-12", "6/12"),
                    ("col-md-7 col-xs-12", "7/12"),
                    ("col-md-8 col-xs-12", "8/12"),
                    ("col-md-9 col-xs-12", "9/12"),
                    ("col-md-10 col-xs-12", "10/12"),
                    ("col-md-11 col-xs-12", "11/12"),
                    ("col-md-12 col-xs-12", "12/12"),
                ],
                default="col-md-12 col-xs-12",
                max_length=30,
                verbose_name="colonne",
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="permissions",
            field=core.models.fields.model_select_to_multiple_field.ModelSelect2Multiple(
                blank=True, to="core.permission", verbose_name="permissions"
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="template",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completion',
                verbose_name="modèle",
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="view",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completion',
                verbose_name="vue",
            ),
        ),
    ]