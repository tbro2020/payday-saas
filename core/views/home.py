from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.db.models import Q, Sum, Count
from datetime import date, timedelta
from employee.models import *
from django.apps import apps

@method_decorator(cache_page(60 * 15), name='dispatch')
class Home(BaseView):
    today = date.today()

    def retired(self, qs, period=0):
        carrer = self.today - timedelta(days=(30*12*35) - (30*period))
        old = self.today - timedelta(days=(30*12*65) - (30*period))
        return qs.filter(
            Q(Q(date_of_join__month=carrer.month) & Q(date_of_join__year=carrer.year)) |
            Q(date_of_birth__month=old.month) & Q(date_of_birth__year=old.year)
        )
    
    def leave(self, qs, period=0):
        when = self.today + timedelta(days=30*period)
        return qs.filter(date_of_join__month=when.month)

    
    def get(self, request):
        ItemPaid = apps.get_model('payroll', 'ItemPaid')
        Payroll = apps.get_model('payroll', 'Payroll')
        
        employees = Employee.objects.all().select_related().prefetch_related()
        
        employees_by_statues = employees.values('status__name')\
            .exclude(status__name=None).annotate(count=Count('status__name'))
        
        itempaid = ItemPaid.objects.filter(created_at__year=self.today.year)
        payrolls = Payroll.objects.filter(created_at__year=self.today.year)
        
        at_this_day = payrolls.aggregate(total=Sum('overall_net'))
        ipr = itempaid.filter(name__icontains='impot').aggregate(total=Sum('amount_qp_employee'))
        cnss = itempaid.filter(name__icontains='inss').aggregate(total=Sum('amount_qp_employer'))

        employees = employees.filter(status__name='EN SERVICE')

        leave_this_month = self.leave(employees)
        leave_in_three_months = self.leave(employees, 3)
        leave_in_six_months = self.leave(employees, 6)

        retired_this_month = self.retired(employees)
        retired_in_three_months = self.retired(employees, 30*3)
        retired_in_six_months = self.retired(employees, 30*6)

        return render(request, "home.html", locals())