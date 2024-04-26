from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import Http404

from core.models.fields import ModelSelect
from core.views import BaseView
from django.apps import apps

from employee.models import *
from payroll.models import *

from django.db import transaction
from pandas import DataFrame
import json


class Synthesis(BaseView):
    organization = {'name': 'ONATRA S.A'}
    branches = Branch.objects.values()

    @transaction.atomic
    def by_item(self, request, pk):
        query = request.GET.dict()
        obj = get_object_or_404(Payroll, id=pk)

        groupby, branches = dict(), self.branches
        items = ItemPaid.objects \
                    .exclude(amount_qp_employee=0) \
                    .filter(payslip__payroll=obj).values('code', 'name').distinct()
        
        for item in items:
            group = item.get('name')
            if group not in groupby: groupby[group] = {}
            
            paid = ItemPaid.objects.filter(payslip__payroll=obj, code=item.get('code', None))
            groupby[group]['AGENT'] = paid.count()

            for branch in branches:
                amount = paid.filter(payslip__employee__branch_id=branch.get('id')) \
                            .aggregate(amount=Sum('amount_qp_employee')).get('amount', 0)
                if amount == 0.0: continue
                groupby[group][branch.get('name')] = round(amount or 0.0, 2)
            groupby[group]['TOTAL'] = round(sum([o for o in groupby[group].values()]) or 0.0, 2)

        df = DataFrame(groupby)
        df.loc[:,'TOTAL'] = df.sum(numeric_only=True, axis=1).round(2)
        groupby = dict(json.loads(df.to_json(orient="columns")))
        groupby['TOTAL']['AGENT'] = obj.payslip_set.count()
        return render(request, "payroll/synthesis.html", locals())

    @transaction.atomic
    def by_employee_field(self, request, pk):
        query = request.GET.dict()
        obj = get_object_or_404(Payroll, id=pk)
        qs = obj.payslip_set.select_related().all()

        field = query.get('by_employee_field')
        groupby, branches = dict(), self.branches
        
        model = Employee._meta.get_field(field)
        model = apps.get_model('employee', model_name=model.remote_field.model._meta.model_name) if isinstance(model, ModelSelect) else None
        
        for group in qs.values_list(f'employee__{field}', flat=True).distinct():
            group = get_object_or_404(model, pk=group) if model else group
            if group not in groupby: groupby[group] = {}
            
            _obj = Payslip.objects.filter(**{f'employee__{field}':group})
            groupby[group]['AGENT'] = _obj.count()
            for branch in branches:
                amount = _obj.filter(employee__branch_id=branch.get('id')).aggregate(amount=Sum('net')).get('amount', 0)
                groupby[group][branch.get('name')] = round(amount or 0.0, 2)
            groupby[group]['TOTAL'] = round(sum([o for o in groupby[group].values()]) or 0.0, 2)
            
            
        df = DataFrame(groupby)
        df.loc[:,'TOTAL'] = df.sum(numeric_only=True, axis=1).round(2)
        groupby = dict(json.loads(df.to_json(orient="columns")))
        return render(request, "payroll/synthesis.html", locals())

    def get(self, request, pk):
        query = request.GET.dict()
        field = list(query.keys())
        if not field: raise Http404
        return getattr(self, field[-1])(request, pk)