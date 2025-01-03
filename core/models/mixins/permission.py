from collections.abc import Iterable

from django.utils.translation import gettext as _
from django.contrib.auth import models
from core.models import fields
from django.apps import apps
from django.db.models import Q

class PermissionsMixin(models.PermissionsMixin):
    groups, user_permissions = None, None

    roles = fields.ModelSelect2Multiple(
        'core.role', 
        verbose_name=_('rôles'), 
        blank=True
    )

    is_staff = fields.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    class Meta:
        abstract = True
    
    def get_user_permissions(self, obj=None, *args, **kwargs):
        """
        Return of permission that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permission = apps.get_model('core', 'permission')
        roles = self.roles.all().values_list('id', flat=True)
        return permission.objects\
            .filter(Q(role__id__in=roles) | Q(user=self))\
            .filter(**kwargs)

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return self.roles.all().values_list('id', flat=True)

    def get_all_permissions(self, obj=None):
        permission = apps.get_model('core', 'permission')
        roles = self.roles.all().values_list('id', flat=True)
        return permission.objects\
            .filter(Q(role__id__in=roles) | Q(user=self))

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        app, model = perm.split('.')
        action, model = model.split('_')
        return self.get_user_permissions().filter(
            content_type__app_label=app,
            content_type__model=model,
            **{action: True}
        ).exists()

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not isinstance(perm_list, Iterable) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)