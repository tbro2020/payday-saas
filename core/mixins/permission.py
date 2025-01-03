from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin

class PermissionMixin(PermissionRequiredMixin):
    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)