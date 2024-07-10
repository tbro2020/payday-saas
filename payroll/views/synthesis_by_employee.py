from django.shortcuts import render, get_object_or_404
from core.views import BaseView
from django.apps import apps

from employee.models import *
from payroll.models import *

from django.db import transaction
from django.apps import apps
import pandas as pd

intcomma = lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x

class SynthesisByEmployee(BaseView):
    
    @transaction.atomic
    def get(self, request, pk):
        query = request.GET.dict()
        field = query.pop('field')

        Payroll = apps.get_model('payroll', 'payroll')
        ItemPaid = apps.get_model('payroll', 'itempaid')

        obj = get_object_or_404(Payroll, id=pk)

        name = f'payslip__employee__{field}'
        #if field in ['gender', 'marital_status']: name = name.replace('__name', '')

        qs = ItemPaid.objects \
            .exclude(amount_qp_employee=0) \
            .filter(payslip__payroll=obj) \
            .filter(**{f'payslip__employee__{k}__name':v for k, v in query.items()}) \
            .values('code', name, 'payslip__employee__grade__category', 'amount_qp_employee')

        # Convert to DataFrame        
        df = pd.DataFrame(qs)

        # Create a pivot table and overwrite the main DataFrame
        df = df.pivot_table(
            index=name, 
            columns='payslip__employee__grade__category', 
            values='amount_qp_employee', 
            aggfunc='sum', 
            fill_value=0
        )

        # Add a 'Total' column that sums across the rows
        df['Total'] = df.sum(axis=1)

        # Create a total row that sums across the columns
        total_row = df.sum(axis=0)
        total_row.name = 'Total'

        # Append the total row to the DataFrame
        df = pd.concat([df, total_row.to_frame().T])

        # Reset the index to remove the name multi-index for better readability (optional)
        df.reset_index(inplace=True)

        # Rename the 'index' column to 'name'
        df.rename(columns={'index': 'Name'}, inplace=True)

        """df.rename(columns={
            'index': 'name',
            'CADRE COLLABORATION': 'CADRE',
            'CADRE DIRECTION': 'DIRIGEANTS'
        }, inplace=True)
        
        df = df[['name', 'DIRIGEANTS', 'CADRE', 'MAITRISE', 'EXECUTANT', 'Total']]"""

        # Flatten the columns: Convert multi-index to a single level
        df.columns.name = None  # Remove column index name if it exists

        # Rename columns to flatten and make them more readable
        df.columns = [col if col != '' else 'Name' for col in df.columns]
        df = df.applymap(intcomma)

        df = df.to_html(index=False, classes='table table-striped mt-3')
        df = df.replace('text-align: right;', 'text-align: left;')

        field = Employee._meta.get_field(field.split('__')[0])
        print(field)

        return render(request, "payroll/synthesis.html", locals())

        """
        # Perform group by operation
        df = df.groupby([name]).agg(
            nombre=('payslip', 'nunique'),
            total=('amount_qp_employee', 'sum')
        ).reset_index()

        # Calculate totals
        total_count = qs.values('payslip').distinct().count()
        total_sum = round(df['total'].sum(), 2)

        totals_df = pd.DataFrame({
            name: ['Total'],
            'nombre': [total_count],
            'total': [total_sum]
        })

        df = pd.concat([df, totals_df], ignore_index=True)

        for column in ['total']:
            df[column] = df[column].apply(intcomma)

        df = df.to_html(index=False, classes='table table-striped mt-3')
        df = df.replace('<th>', '<th style="text-align: left;" class="text-capitalize">')

        return render(request, "payroll/synthesis.html", locals())
        """