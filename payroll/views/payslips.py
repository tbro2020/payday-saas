from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Sum
from core.views import Change

from payroll.filters import PayslipFilter
from employee.models import Employee
from django.apps import apps


class Payslips(Change):
    template_name = 'payroll/payslips.html'

    def documents(self):
        _model = apps.get_model('core', 'template')
        return _model.objects.filter(**{
            'content_type__app_label': 'payroll',
            'content_type__model__in': ['payroll', 'payslip']
        }).values('id', 'name', 'content_type__model')
    
    def sheets(self):
        data = [field for field in Employee._meta.fields if field.get_internal_type() == 'ModelSelect']
        return [{'name': field.name+'__name', 'verbose_name': field.verbose_name} for field in data]
    
    sheet_fields = {
        'employee__direction__name': _('Département'),
        'employee__payer_name__name': _('Banque'),
        'employee__branch__name': _('Zone'),
        'employee__grade__name': _('Grade'),
        'employee__grade__category': _('Grade par catégorie'),
    }
    
    def duties(self):
        ItemPaid = apps.get_model('payroll', 'ItemPaid')
        return ItemPaid.objects.filter(payslip__payroll=self.kwargs['pk'])\
            .filter(amount_qp_employee__lte=0).values('name', 'code').distinct()
    
    def items(self):
        ItemPaid = apps.get_model('payroll', 'ItemPaid')
        return list(ItemPaid.objects.filter(payslip__payroll=self.kwargs['pk'])\
            .filter(amount_qp_employee__gte=0).values('name', 'code').distinct())
    
    def get(self, request, pk):
        app, model = 'payroll', 'payroll'
        self.kwargs['app'], self.kwargs['model'] = app, model
        app, model = 'payroll', apps.get_model('payroll', 'payroll')
        Payslip = apps.get_model(app, 'payslip')

        obj = get_object_or_404(model, id=pk)
        query = {k:v for k, v in request.GET.items() if v}
        qs = obj.payslip_set.all().select_related().prefetch_related()
        filter = PayslipFilter(query, queryset=qs)

        qs = filter.qs
        fields = [field.name for field in qs.model._meta.fields]
        qs = qs.filter(**{k:v for k,v in query.items() if k in fields})

        overall_net = round(qs.aggregate(amount=Sum('net'))['amount'] or 0, 2)
        count = qs.count()

        paginator = Paginator(qs.order_by(f'-{Payslip._meta.pk.name}'), 100)
        qs = paginator.page(int(request.GET.dict().get('page', 1)))
        
        return render(request, self.template_name, locals())