from django.shortcuts import render, redirect, get_object_or_404
from core.views import BaseView
from payroll.models import *
import pandas as pd

from django.apps import apps

intcomma = lambda value: "{:,}".format(round(abs(value), 2))

class Listing(BaseView):
    def get(self, request, pk):
        qs = []
        Payroll = apps.get_model('payroll', 'payroll')
        ItemPaid = apps.get_model('payroll', 'itempaid')

        query = request.GET.dict()
        obj = get_object_or_404(Payroll, id=pk)
        
        code = query.pop('code')
        item = Item.objects.filter(code=code).first()
        if not code: return redirect(reversed('payroll:payslips', kwargs={'pk': obj.pk}))

        qs = ItemPaid.objects.filter(code=item.code, payslip__payroll=obj) \
            .filter(**{f'payslip___employee__{k}__name':v for k,v in query.items()}) \
            .values('payslip___employee__registration_number', 'payslip___employee__last_name', 'payslip___employee__middle_name', 'amount_qp_employee', 'amount_qp_employer')
        
        df = pd.DataFrame(qs)

        # Calculate the sums
        sum_amount_qp_employee = df['amount_qp_employee'].sum()
        sum_amount_qp_employer = df['amount_qp_employer'].sum()

        total_df = pd.DataFrame({
            'payslip___employee__registration_number': ['Total'],
            'payslip___employee__last_name': [''],
            'payslip___employee__middle_name': [''],
            'amount_qp_employee': [sum_amount_qp_employee],
            'amount_qp_employer': [sum_amount_qp_employer]
        })

        df = pd.concat([df, total_df], ignore_index=True)

        for column in ['amount_qp_employee', 'amount_qp_employer']:
            df[column] = df[column].apply(intcomma)

        df = df.to_html(index=False, classes='table table-striped mt-3')
        df = df.replace('<th>', '<th style="text-align: left;" class="text-capitalize">')

        return render(request, "payroll/listing.html", locals())
