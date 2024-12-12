from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.utils.text import slugify
from core.views import BaseView

from payroll.filters import PayslipFilter
from employee.models import Employee

from django.apps import apps
import pandas as pd
import json

class Sheet(BaseView):
    
    def sheet(self, obj, query):
        rows = []
        ItemPaid = apps.get_model('payroll', 'ItemPaid')

        # Simplify employee_list_display
        employee_list_display = ['registration_number', 'social_security_number', 'first_name', 'middle_name', 'last_name']
        employee_list_display = [field for field in Employee._meta.fields if field.name in employee_list_display]

        # Combine fields with choices or ModelSelect
        employee_list_display += [field for field in Employee._meta.fields if field.choices or field.get_internal_type() == 'ModelSelect']

        # Fetch payslips and related items
        qs = obj.payslip_set.all().select_related().prefetch_related()
        qs = PayslipFilter(query, queryset=qs).qs

        fields = [field.name for field in qs.model._meta.fields]
        qs = qs.filter(**{k:v for k,v in query.items() if k in fields})

        for payslip in qs:
            items_paid = payslip.itempaid_set.all().values('name', 'amount_qp_employee')
            row = {field.verbose_name.title(): getattr(payslip.employee, field.name).name
                    if hasattr(getattr(payslip.employee, field.name), 'name') else 
                    getattr(payslip.employee, field.name)
                   for field in employee_list_display}
            
            for item in items_paid:
                row[item['name'].title()] = item['amount_qp_employee']

            payslip_list_display = (field for field in payslip._meta.model._meta.fields if field.get_internal_type() == 'FloatField')
            row.update({field.verbose_name.title(): getattr(payslip, field.name) for field in payslip_list_display})

            rows.append(row)
        return rows

    def get(self, request, pk):
        Payroll = apps.get_model('payroll', 'payroll')
        obj = get_object_or_404(Payroll, id=pk)

        query = request.GET.dict()
        group_by = query.pop('group_by', None)

        data = self.sheet(obj, query)
        df = pd.read_json(json.dumps(data))
        df = df.groupby(group_by) if group_by else df

        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="sheet_{group_by if group_by else 'global'}.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            [group.to_excel(writer, sheet_name=slugify(str(row)), index=False) 
                for row, group in df] if group_by else df.to_excel(writer, index=False)
        return response
