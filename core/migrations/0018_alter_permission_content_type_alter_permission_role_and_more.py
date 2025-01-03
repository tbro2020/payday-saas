# Generated by Django 5.1.3 on 2024-12-30 08:28

import core.models.fields.booleanfield
import core.models.fields.charfield
import core.models.fields.datetimefield
import core.models.fields.foreignkey
import core.models.fields.jsonfield
import core.models.fields.model_select_field
import core.models.fields.textfield
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0017_historicalwidget_content_type_widget_content_type_and_more"),
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
            name="content_type",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
                verbose_name="content type",
            ),
        ),
        migrations.CreateModel(
            name="Notification",
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
                    "redirect",
                    core.models.fields.charfield.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="redirect to",
                    ),
                ),
                (
                    "subject",
                    core.models.fields.charfield.CharField(
                        max_length=255, verbose_name="subject"
                    ),
                ),
                (
                    "viewed",
                    core.models.fields.booleanfield.BooleanField(
                        default=False, verbose_name="seen"
                    ),
                ),
                (
                    "message",
                    core.models.fields.textfield.TextField(verbose_name="message"),
                ),
                (
                    "_from",
                    core.models.fields.model_select_field.ModelSelectField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="from",
                    ),
                ),
                (
                    "_to",
                    core.models.fields.model_select_field.ModelSelectField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="to",
                    ),
                ),
                (
                    "created_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
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
                    "updated_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        on_update=True,
                        related_name="%(app_label)s_%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "notification",
                "verbose_name_plural": "notifications",
                "ordering": ["-created_at"],
            },
        ),
    ]