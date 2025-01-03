# Generated by Django 5.1.3 on 2024-12-29 10:56

import core.models.fields.ace_field
import core.models.fields.foreignkey
import core.models.fields.integerfield
import core.models.fields.model_select_field
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0015_permission_level_alter_permission_add_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalwidget",
            name="active",
        ),
        migrations.RemoveField(
            model_name="widget",
            name="active",
        ),
        migrations.RemoveField(
            model_name="widget",
            name="permissions",
        ),
        migrations.AlterField(
            model_name="historicalwidget",
            name="template",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completionpress "Ctrl+M" to toggle in modal mode',
                verbose_name="modèle",
            ),
        ),
        migrations.AlterField(
            model_name="historicalwidget",
            name="view",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completionpress "Ctrl+M" to toggle in modal mode',
                verbose_name="vue",
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="job",
            field=core.models.fields.ace_field.AceField(
                default="0",
                help_text='press "Ctrl+Space" to get code completionpress "Ctrl+M" to toggle in modal mode',
                verbose_name="job",
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
            name="level",
            field=core.models.fields.integerfield.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(10),
                ],
                verbose_name="niveau",
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
            model_name="widget",
            name="template",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completionpress "Ctrl+M" to toggle in modal mode',
                verbose_name="modèle",
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="view",
            field=core.models.fields.ace_field.AceField(
                help_text='press "Ctrl+Space" to get code completionpress "Ctrl+M" to toggle in modal mode',
                verbose_name="vue",
            ),
        ),
    ]
