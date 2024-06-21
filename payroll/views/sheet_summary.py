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

    fields = {
        '_employee__direction__name': 'Departement',
        '_employee__payer_name__name': 'Banque',
        '_employee__branch__name': 'Zone',
        '_employee__grade__name': 'Grade',
    }
    
    def sheet(self, obj, query):
        rows = []
        ItemPaid = apps.get_model('payroll', 'ItemPaid')

        # Fetch payslips and related items
        qs = obj.payslip_set.all().select_related().prefetch_related()
        qs = PayslipFilter(query, queryset=qs).qs

        fields = [field.name for field in qs.model._meta.fields]
        qs = qs.filter(**{k:v for k,v in query.items() if k in fields})

        return qs.values(**[
            '_employee__registration_number',
            '_employee__middle_name',
            '_employee__last_name',

            '_employee__branch__name',
            '_employee__grade__name',

            '_employee__payer_name__name',
            '_employee__payment_account',

            'net'
        ])

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
