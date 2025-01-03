# Generated by Django 5.1.3 on 2024-12-27 12:59

import core.models.fields.charfield
import core.models.fields.datetimefield
import core.models.fields.foreignkey
import core.models.fields.jsonfield
import core.models.fields.model_select_field
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0001_initial"),
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
        migrations.CreateModel(
            name="RowLevel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "_metadata",
                    core.models.fields.jsonfield.JSONField(
                        blank=True, default=dict, verbose_name="metadata"
                    ),
                ),
                (
                    "updated_at",
                    core.models.fields.datetimefield.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "created_at",
                    core.models.fields.datetimefield.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                (
                    "field",
                    core.models.fields.charfield.CharField(
                        max_length=255, verbose_name="champ"
                    ),
                ),
                (
                    "value",
                    core.models.fields.charfield.CharField(
                        max_length=255, verbose_name="value"
                    ),
                ),
                (
                    "content_type",
                    core.models.fields.foreignkey.ForeignKey(
                        default=None,
                        limit_choices_to={
                            "app_label__in": ["core", "employee", "payroll"]
                        },
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="rows",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
                (
                    "organization",
                    core.models.fields.foreignkey.ForeignKey(
                        blank=True,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.organization",
                        verbose_name="organization",
                    ),
                ),
                (
                    "user",
                    core.models.fields.model_select_field.ModelSelectField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="rows",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "ligne",
                "verbose_name_plural": "lignes",
                "unique_together": {("content_type", "user", "field")},
            },
        ),
        migrations.DeleteModel(
            name="Row",
        ),
    ]