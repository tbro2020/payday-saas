from django.shortcuts import render, get_object_or_404
from core.filters import filter_set_factory
from django.core.paginator import Paginator
from django.db.models import Sum
from core.views import Change


from employee.models import Employee
from payroll.models import *



class Payslips(Change):
    template_name = 'payroll/payslips.html'
    
    def sheets(self):
        return [field for field in Employee._meta.fields if field.choices or field.get_internal_type() == 'ModelSelect']
    
    def duties(self):
        return ItemPaid.objects.filter(payslip__payroll=self.kwargs['pk'])\
            .filter(amount_qp_employee__lte=0).values('name', 'code').distinct()
    
    def items(self):
        return list(ItemPaid.objects.filter(payslip__payroll=self.kwargs['pk'])\
            .filter(amount_qp_employee__gte=0).values('name', 'code').distinct())
    
    def get(self, request, pk):
        self.kwargs['app'], self.kwargs['model'] = 'payroll', 'payroll'
        app, model = 'payroll', Payroll

        obj = get_object_or_404(Payroll, id=pk)
        qs = Payslip.objects.filter(payroll=obj)
        
        list_filter = getattr(Payslip, 'list_filter', [])
        
        query = {k:v for k, v in request.GET.items() if v}
        for key in list(query.keys()):
            if key in ['employee__date_of_birth', 'employee__date_of_join']:
                year, month = query.pop(key).split('-')
                query['%s__month' % key] = month
                query['%s__year' % key] = year

        qs_filter = filter_set_factory(Payslip, fields=list_filter)
        qs_filter = qs_filter(query, queryset=qs)
        qs = qs_filter.hard_filter()

        overall_net = round(qs.aggregate(amount=Sum('net'))['amount'] or 0, 2)
        count = qs.count()


        paginator = Paginator(qs.order_by(f'-{Payslip._meta.pk.name}'), 25)
        qs = paginator.page(int(request.GET.dict().get('page', 1)))
        
        return render(request, self.template_name, locals())