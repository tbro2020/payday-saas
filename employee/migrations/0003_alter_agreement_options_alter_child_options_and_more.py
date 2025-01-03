# Generated by Django 5.1.3 on 2024-12-27 09:30

import core.models.fields.charfield
import core.models.fields.datefield
import core.models.fields.datetimefield
import core.models.fields.filefield
import core.models.fields.foreignkey
import core.models.fields.integerfield
import core.models.fields.model_select_field
import core.models.fields.onetoonefield
import core.models.fields.textfield
import core.utils.upload_directory_file
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import employee.utils.default_registration_number
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_contenttypeapprover_content_type_and_more"),
        ("employee", "0002_employee_email"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agreement",
            options={"verbose_name": "contract", "verbose_name_plural": "contracts"},
        ),
        migrations.AlterModelOptions(
            name="child",
            options={"verbose_name": "child", "verbose_name_plural": "children"},
        ),
        migrations.AlterModelOptions(
            name="direction",
            options={
                "verbose_name": "department",
                "verbose_name_plural": "departments",
            },
        ),
        migrations.AlterModelOptions(
            name="employee",
            options={"verbose_name": "employee", "verbose_name_plural": "employees"},
        ),
        migrations.AlterModelOptions(
            name="status",
            options={"verbose_name": "status", "verbose_name_plural": "status"},
        ),
        migrations.AlterModelOptions(
            name="subdirection",
            options={
                "verbose_name": "sub-division",
                "verbose_name_plural": "sub-divisions",
            },
        ),
        migrations.RemoveField(
            model_name="agreement",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="branch",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="child",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="designation",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="direction",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="document",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="grade",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="service",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="status",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="subdirection",
            name="approved",
        ),
        migrations.AlterField(
            model_name="agreement",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="birth_certificate",
            field=core.models.fields.filefield.FileField(
                upload_to=core.utils.upload_directory_file,
                verbose_name="birth certificate",
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="date_of_birth",
            field=core.models.fields.datefield.DateField(verbose_name="date of birth"),
        ),
        migrations.AlterField(
            model_name="child",
            name="employee",
            field=core.models.fields.model_select_field.ModelSelectField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.employee",
                verbose_name="employee",
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="full_name",
            field=core.models.fields.charfield.CharField(
                max_length=100, verbose_name="full name"
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="child",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="designation",
            name="working_days_per_month",
            field=core.models.fields.integerfield.IntegerField(
                default=23, verbose_name="working days per month"
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="direction",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="employee",
            field=core.models.fields.model_select_field.ModelSelectField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.employee",
                verbose_name="employee",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="agreement",
            field=core.models.fields.model_select_field.ModelSelectField(
                on_delete=django.db.models.deletion.CASCADE,
                to="employee.agreement",
                verbose_name="contract type",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="comment",
            field=core.models.fields.textfield.TextField(
                blank=True, default=None, null=True, verbose_name="comment"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="date_of_birth",
            field=core.models.fields.datefield.DateField(
                default=None,
                help_text="YYYY-MM-DD",
                null=True,
                verbose_name="date of birth",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="date_of_join",
            field=core.models.fields.datefield.DateField(
                default=None,
                help_text="YYYY-MM-DD",
                null=True,
                verbose_name="hire date",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="direction",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.direction",
                verbose_name="department",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="emergency_information",
            field=core.models.fields.textfield.TextField(
                default=None, null=True, verbose_name="emergency information"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="first_name",
            field=core.models.fields.charfield.CharField(
                blank=True,
                default=None,
                max_length=100,
                null=True,
                verbose_name="first name",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="gender",
            field=core.models.fields.charfield.CharField(
                choices=[("male", "male"), ("female", "female")],
                max_length=10,
                verbose_name="gender",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="last_name",
            field=core.models.fields.charfield.CharField(
                blank=True, default=None, max_length=100, null=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="marital_status",
            field=core.models.fields.charfield.CharField(
                choices=[
                    ("maried", "married"),
                    ("single", "single"),
                    ("widower", "widowed"),
                ],
                max_length=12,
                verbose_name="marital status",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="middle_name",
            field=core.models.fields.charfield.CharField(
                blank=True,
                default=None,
                max_length=100,
                null=True,
                verbose_name="surname",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="mobile_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default=None,
                max_length=128,
                null=True,
                region=None,
                verbose_name="mobile phone number",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="payer_name",
            field=core.models.fields.charfield.CharField(
                default=None, max_length=50, null=True, verbose_name="payer's name"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="payment_account",
            field=core.models.fields.charfield.CharField(
                blank=True,
                default=None,
                max_length=50,
                null=True,
                verbose_name="account/payment number",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="payment_method",
            field=core.models.fields.charfield.CharField(
                choices=[
                    ("cash", "cash"),
                    ("bank", "bank"),
                    ("mobile Money", "mobile Money"),
                ],
                max_length=20,
                verbose_name="payment method",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="physical_address",
            field=core.models.fields.textfield.TextField(
                blank=True, default=None, null=True, verbose_name="physical address"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="registration_number",
            field=core.models.fields.charfield.CharField(
                default=employee.utils.default_registration_number,
                max_length=50,
                unique=True,
                verbose_name="registration number",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="social_security_number",
            field=core.models.fields.charfield.CharField(
                blank=True,
                default=None,
                max_length=50,
                null=True,
                verbose_name="social security number",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="spouse",
            field=core.models.fields.charfield.CharField(
                blank=True,
                default=None,
                max_length=100,
                null=True,
                verbose_name="spouse",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="spouse_date_of_birth",
            field=core.models.fields.datefield.DateField(
                blank=True,
                default=None,
                help_text="YYYY-MM-DD",
                null=True,
                verbose_name="spouse's date of birth",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="status",
            field=core.models.fields.model_select_field.ModelSelectField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.status",
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="sub_direction",
            field=core.models.fields.model_select_field.ModelSelectField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.subdirection",
                verbose_name="sub-division",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="user",
            field=core.models.fields.onetoonefield.OneToOneField(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="sub_direction",
            field=core.models.fields.model_select_field.ModelSelectField(
                on_delete=django.db.models.deletion.CASCADE,
                to="employee.subdirection",
                verbose_name="sub-division",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="name",
            field=core.models.fields.charfield.CharField(
                max_length=100, unique=True, verbose_name="name"
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="created_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="direction",
            field=core.models.fields.model_select_field.ModelSelectField(
                on_delete=django.db.models.deletion.CASCADE,
                to="employee.direction",
                verbose_name="department",
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="name",
            field=models.CharField(max_length=100, unique=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="organization",
            field=core.models.fields.foreignkey.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="updated_at",
            field=core.models.fields.datetimefield.DateTimeField(
                auto_now=True, verbose_name="updated at"
            ),
        ),
        migrations.AlterField(
            model_name="subdirection",
            name="updated_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                on_update=True,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
    ]
