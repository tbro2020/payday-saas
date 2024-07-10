from django.shortcuts import render, get_object_or_404
from core.views import BaseView

from employee.models import *
from payroll.models import *

from django.db import transaction
from django.apps import apps
import pandas as pd


# intcomma = lambda value: "{:,}".format(round(value, 2))
intcomma = lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x

class SynthesisByItem(BaseView):

    @transaction.atomic
    def get(self, request, pk):
        Payroll = apps.get_model('payroll', 'payroll')
        ItemPaid = apps.get_model('payroll', 'itempaid')

        query = request.GET.dict()
        obj = get_object_or_404(Payroll, id=pk)

        qs = ItemPaid.objects \
            .exclude(amount_qp_employee=0) \
            .filter(payslip__payroll=obj) \
            .filter(**{f'payslip__employee__{k}__name':v for k, v in query.items()}) \
            .values('code', 'name', 'payslip', 'payslip__employee__grade__category', 'amount_qp_employee')
        
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(qs)

        # Create a pivot table and overwrite the main DataFrame
        df = df.pivot_table(
            index='name', 
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

        # Flatten the columns: Convert multi-index to a single level
        df.columns.name = None  # Remove column index name if it exists

        # Rename columns to flatten and make them more readable
        df.columns = [col if col != '' else 'Name' for col in df.columns]
        df = df.applymap(intcomma)

        df = df.to_html(index=False, classes='table table-striped mt-3')
        df = df.replace('text-align: right;', 'text-align: left;')

        field = {'verbose_name': 'Éléments de paie'}

        return render(request, "payroll/synthesis.html", locals())