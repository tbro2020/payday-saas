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

class SheetSummary(BaseView):
    
    def sheet(self, obj, query):
        rows = []
        ItemPaid = apps.get_model('payroll', 'ItemPaid')

        # Fetch payslips and related items
        qs = obj.payslip_set.all().select_related().prefetch_related()
        qs = PayslipFilter(query, queryset=qs).qs

        fields = [field.name for field in qs.model._meta.fields]
        qs = qs.filter(**{k:v for k,v in query.items() if k in fields})

        return qs.filter(net__gt=0).values(
            '_employee__registration_number',

            '_employee__last_name',
            '_employee__middle_name',

            '_employee__direction__name',
            '_employee__branch__name',
            '_employee__grade__name',

            '_employee__payer_name__name',
            '_employee__payment_account',

            'net'
        ).order_by('_employee__registration_number')

    def get(self, request, pk):
        Payroll = apps.get_model('payroll', 'payroll')
        obj = get_object_or_404(Payroll, id=pk)

        query = request.GET.dict()
        group_by = query.pop('group_by', None)

        data = self.sheet(obj, query)
        df = pd.DataFrame(list(data))
        columns = {
            '_employee__registration_number' : 'matricule',

            '_employee__last_name': 'nom',
            '_employee__middle_name': 'post nom',
            

            '_employee__direction__name': 'departement',
            '_employee__branch__name': 'zone',
            '_employee__grade__name': 'grade',

            '_employee__payer_name__name': 'banque',
            '_employee__payment_account': 'n. Compte',

            'net': 'net'
        }
        
        df.columns = [columns.get(col, col) for col in df.columns]
        group_by = columns[group_by]

        df = df.groupby(group_by) if group_by else df

        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="sheet_{group_by if group_by else 'global'}.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            [group.to_excel(writer, sheet_name=slugify(str(row)), index=False) 
                for row, group in df] if group_by else df.to_excel(writer, index=False)
        return response
