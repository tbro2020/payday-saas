from django.shortcuts import redirect, reverse, get_object_or_404
from django.utils.translation import gettext as _
from django.shortcuts import HttpResponse
from django.utils.text import slugify
from core.views import BaseView

from payroll.models import *
from payroll.tasks import *



import pandas as pd
import json
import io

class Sheet(BaseView):
    def get(self, request, pk):
        obj = get_object_or_404(Payroll, id=pk)
        group_by = request.GET.get('group_by', None)

        output = io.BytesIO()
        df = pd.read_json(json.dumps(obj.sheet()))
        df = df.groupby(group_by) if group_by else df

        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="sheet_{group_by if group_by else 'global'}.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            [group.to_excel(writer, sheet_name=slugify(str(row)), index=False) 
                for row, group in df] if group_by else df.to_excel(writer, index=False)
        return response
