from django.http import HttpResponse
from core.views import BaseView

from employee.models import Employee
import pandas as pd

from django.utils.text import slugify
import json

class Canvas(BaseView):
    def get(self, request):
        query = {k:v.split(',') if '__in' in k else v  for k,v in request.GET.dict().items() if v}
        qs = Employee.objects.filter(**query) \
            .values('registration_number', 'last_name', 'middle_name', 'branch__name', 'grade__name')
        
        columns = ['absence', 'absence.justifiee']
        field_no_numbers = []

        data = [{
            'registration_number': obj['registration_number'],
            'last_name': obj['last_name'],
            'middle_name': obj['middle_name'],
            'grade': obj['grade__name'],
            'branch': obj['branch__name'],
            **{k: None if k in field_no_numbers else 0 for k in columns}
        } for obj in qs]

        group_by = 'branch'
        df = pd.read_json(json.dumps(data), dtype={'registration_number': str})

        if not df.empty:
            df = df.sort_values(by=['grade', 'registration_number', 'last_name', 'middle_name'], 
                                ascending=[True, True, True, True])
            df = df.groupby(group_by)
        
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="canvas.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            [group.to_excel(writer, sheet_name=slugify(str(row)), index=False) 
                for row, group in df] if group_by else df.to_excel(writer, sheet_name='global', index=False)
        return response

