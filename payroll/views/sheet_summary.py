from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from payroll.filters import PayslipFilter
from django.utils.text import slugify
from core.views import BaseView

from django.apps import apps
import pandas as pd

class SheetSummary(BaseView):
    
    def sheet(self, obj, query):
        rows = []
        ItemPaid = apps.get_model('payroll', 'ItemPaid')

        # Fetch payslips and related items
        qs = obj.payslip_set.all().select_related().prefetch_related()
        qs = PayslipFilter(query, queryset=qs).qs

        fields = [field.name for field in qs.model._meta.fields]
        qs = qs.filter(**{k:v for k,v in query.items() if k in fields})

        return qs.values(
            'employee__registration_number',

            'employee__last_name',
            'employee__middle_name',

            'employee__direction__name',
            'employee__branch__name',

            'employee__grade__name',
            'employee__grade__category',

            'employee__payer__name',
            'employee__payment_account',

            'net'
        ).order_by(
            'employee__registration_number', 
            'employee__grade__name'
        )

    def get(self, request, pk):
        Payroll = apps.get_model('payroll', 'payroll')
        obj = get_object_or_404(Payroll, id=pk)

        query = request.GET.dict()
        group_by = query.pop('group_by', None)

        data = self.sheet(obj, query)
        df = pd.DataFrame(list(data))

        if not df.empty:
            df['employee__registration_number'] = df['employee__registration_number'].apply(str)

        columns = {
            'employee__registration_number' : 'matricule',

            'employee__last_name': 'nom',
            'employee__middle_name': 'post nom',
            

            'employee__direction__name': 'departement',
            'employee__branch__name': 'zone',
            'employee__grade__name': 'grade',
            'employee__grade__category': 'categorie',

            'employee__payer__name': 'banque',
            'employee__payment_account': 'n. Compte',

            'net': 'net'
        }
        
        df.columns = [columns.get(col, col) for col in df.columns]

        group_by = columns.get(group_by, None)
        df = df.groupby(group_by) if group_by else df

        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="sheet_{group_by if group_by else 'global'}.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            if not group_by:
                df.to_excel(writer, index=False)
            else :
                for row, group in df:
                    sum_net = group['net'].sum()
                    group = pd.concat([group, pd.DataFrame({
                        col: [sum_net if col == 'net' else '']
                        for col in columns.values()
                    })], ignore_index=True)
                    group.to_excel(writer, sheet_name=slugify(str(row)), index=False)
                
            #[group.to_excel(writer, sheet_name=slugify(str(row)), index=False) 
            #    for row, group in df] if group_by else df.to_excel(writer, index=False)

        return response
