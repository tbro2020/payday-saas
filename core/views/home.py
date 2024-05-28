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
        ipr = itempaid.filter(name__icontains='impot').aggregate(total=Sum('amount_qp_employee'))
        cnss = itempaid.filter(name__icontains='inss').aggregate(total=Sum('amount_qp_employer'))

        retired_this_month = employees.all()
        retired_in_three_months = employees.all()
        retired_this_year = employees.all()

        leave_this_month = employees.all()
        leave_in_three_months = employees.all()
        leave_this_year = employees.all()

        return render(request, "home.html", locals())