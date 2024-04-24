from django.shortcuts import redirect, reverse, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib import messages
from core.views import BaseView

from payroll.models import *
from payroll.tasks import *


class Sheet(BaseView):
    def get(self, request, pk):
        obj = get_object_or_404(Payroll, id=pk)
        group_by = request.GET.get('group_by', None)
        sheet.delay(obj.id, request.user.id, group_by)
        messages.success(request, _('Votre demande a été programmé, nous vous préviendrons lorsque votre feuille sera prête.'))
        return redirect(request.META.get('HTTP_REFERER', reverse('payroll:payslips', args=[obj.pk])))
