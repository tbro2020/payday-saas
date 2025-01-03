# Generated by Django 5.1.3 on 2024-12-27 16:43

import core.models.fields.ace_field
import core.models.fields.charfield
import core.models.fields.datetimefield
import core.models.fields.foreignkey
import core.models.fields.html_field
import core.models.fields.jsonfield
import core.models.fields.model_select_field
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0010_alter_role_options_remove_organization_metadata_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.RemoveField(
            model_name="historicaluser",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="historicaluser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="historicaluser",
            name="is_staff",
        ),
        migrations.RemoveField(
            model_name="historicaluser",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="user",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="user",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_permissions",
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
        migrations.CreateModel(
            name="HistoricalTemplate",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
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
                        blank=True, editable=False, verbose_name="updated at"
                    ),
                ),
                (
                    "created_at",
                    core.models.fields.datetimefield.DateTimeField(
                        blank=True, editable=False, verbose_name="created at"
                    ),
                ),
                (
                    "content",
                    core.models.fields.html_field.HTMLField(
                        default=None, null=True, verbose_name="content"
                    ),
                ),
                (
                    "name",
                    core.models.fields.charfield.CharField(
                        db_index=True, max_length=100, verbose_name="name"
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "content_type",
                    core.models.fields.model_select_field.ModelSelectField(
                        blank=True,
                        db_constraint=False,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
                (
                    "created_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        blank=True,
                        db_constraint=False,
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    core.models.fields.foreignkey.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="core.organization",
                        verbose_name="organization",
                    ),
                ),
                (
                    "updated_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        db_constraint=False,
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        on_update=True,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical document template",
                "verbose_name_plural": "historical document templates",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalWidget",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
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
                        blank=True, editable=False, verbose_name="updated at"
                    ),
                ),
                (
                    "created_at",
                    core.models.fields.datetimefield.DateTimeField(
                        blank=True, editable=False, verbose_name="created at"
                    ),
                ),
                (
                    "column",
                    models.CharField(
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "active",
                    models.BooleanField(
                        default=True, help_text="show widget", verbose_name="actif"
                    ),
                ),
                (
                    "template",
                    core.models.fields.ace_field.AceField(
                        help_text='press "Ctrl+Space" to get code completion',
                        verbose_name="modèle",
                    ),
                ),
                (
                    "view",
                    core.models.fields.ace_field.AceField(
                        help_text='press "Ctrl+Space" to get code completion',
                        verbose_name="vue",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "created_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        blank=True,
                        db_constraint=False,
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    core.models.fields.foreignkey.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="core.organization",
                        verbose_name="organization",
                    ),
                ),
                (
                    "updated_by",
                    django_currentuser.db.models.fields.CurrentUserField(
                        db_constraint=False,
                        default=django_currentuser.middleware.get_current_authenticated_user,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        on_update=True,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical widget",
                "verbose_name_plural": "historical widgets",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
