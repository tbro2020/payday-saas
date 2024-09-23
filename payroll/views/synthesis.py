from django.utils.translation import gettext as _
from django.shortcuts import render

from core.views import BaseView
from django.apps import apps
import pandas as pd

intcomma = lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x
get_name_of_fields = lambda _list: list(map(lambda x: x.name, _list))

class Synthesis(BaseView):
    action = ["view"]
    template_name = "payroll/synthesis.html"
    template_name_field_selector = "payroll/field_selector.html"
    
    def get_field_verbose(self, model, field):
        fields = field.split('__')
        if len(fields) == 1:
            return model._meta.get_field(fields[0]).verbose_name.lower()
        model = model._meta.get_field(fields[0]).related_model
        return self.get_field_verbose(model, '__'.join(fields[1:]))
    
    def get_field(self, model, field):
        fields = field.split('__')
        if len(fields) == 1:
            return model._meta.get_field(fields[0])
        model = model._meta.get_field(fields[0]).related_model
        return self.get_field(model, '__'.join(fields[1:]))
    
    def get(self, request, func, pk):
        model = apps.get_model('payroll', 'payslip')
        return render(request, self.template_name_field_selector, locals())
    
    def post(self, request, func, pk):
        obj = apps.get_model('payroll', 'payroll').objects.get(id=pk)
        model = apps.get_model('payroll', 'payslip')

        qs = model.objects.select_related().prefetch_related()
        qs = qs._all(user=request.user, subdomain=request.subdomain) if hasattr(qs, '_all') else qs.all()

        fields = list({k:v for k,v in request.POST.dict().items() if k not in ['csrfmiddlewaretoken']}.values())
        if 'net' not in fields: fields.append('net')
        qs = qs.filter(payroll=obj)
        data = qs.values(*fields)

        fields = {field : self.get_field_verbose(model, field) for field in fields}
        df = pd.DataFrame.from_records(data)

        df = df.pivot_table(
            index=request.POST.get('column'), 
            columns=request.POST.get('row'), 
            values='net', 
            aggfunc=func, 
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
        df.rename(columns=fields, inplace=True)

        # Flatten the columns: Convert multi-index to a single level
        df.columns.name = None  # Remove column index name if it exists

        # Rename columns to flatten and make them more readable
        if func == 'sum': df = df.map(intcomma)

        fields = {field : self.get_field(model, field).model._meta.verbose_name 
                  for field in fields.keys() if field != 'net'}
        
        # Rename the 'index' column to 'name'
        df.rename(columns={'index': fields.get(request.POST.get('row'), '-').title()}, inplace=True)
        fields = fields.values()

        df = df.to_html(index=False, classes='table table-striped mt-3')
        df = df.replace('text-align: right;', 'text-align: left;')

        return render(request, self.template_name, locals())