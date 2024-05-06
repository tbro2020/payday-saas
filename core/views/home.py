from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView

from django.db.models import Sum
from employee.models import *
from payroll.models import *
from datetime import date


class Home(BaseView):
    today = date.today()

    def get(self, request):
        employees = Employee.objects.all()
        itempaid = ItemPaid.objects.filter(created_at__year=self.today.year)
        payrolls = Payroll.objects.filter(created_at__year=self.today.year)
        at_this_day = payrolls.aggregate(total=Sum('overall_net'))

        ipr = itempaid.filter(name__icontains='ipr').aggregate(total=Sum('amount_qp_employee'))
        cnss = itempaid.filter(name__icontains='cnss').aggregate(total=Sum('amount_qp_employer'))

        return render(request, "home.html", locals())