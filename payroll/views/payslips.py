from django.shortcuts import render, get_object_or_404
from core.filters import filter_set_factory
from django.core.paginator import Paginator
from core.views import BaseView
from django.db.models import Q

from employee.models import Employee
from payroll.models import *

class Payslips(BaseView):
    
    def sheet_fields(self):
        return [field for field in Employee._meta.fields if field.name == 'payer_name' or
                                                            field.choices or field.get_internal_type() == 'ModelSelect']
    
    def duties(self):
        return DutyItem.objects.values('name', 'pk')
    
    def items(self):
        return Item.objects.filter(Q(is_taxable=True)
                                   |Q(is_social_security=True)).values('name', 'pk')
    
    def get(self, request, pk):
        app = 'payroll'
        model = Payroll
        
        obj = get_object_or_404(Payroll, id=pk)
        qs = Payslip.objects.filter(payroll=obj)
        count = qs.count()
        
        list_filter = getattr(Payslip, 'list_filter', [])
        qs_filter = filter_set_factory(Payslip, fields=list_filter)
        qs_filter = qs_filter(request.GET, queryset=qs)
        qs = qs_filter.qs
        
        paginator = Paginator(qs, 25)
        qs = paginator.page(int(request.GET.dict().get('page', 1)))
        
        return render(request, 'payroll/payslips.html', locals())