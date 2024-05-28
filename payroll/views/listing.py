from django.shortcuts import render, redirect, get_object_or_404
from core.views import BaseView
from payroll.models import *


class Listing(BaseView):
    def get(self, request, pk):
        qs = []
        query = request.GET.dict()
        obj = get_object_or_404(Payroll, id=pk)
        
        code = query.pop('code')
        if not code: return redirect(reversed('payroll:payslips', kwargs={'pk': obj.pk}))

        qs = [{
            'registration_number': _obj.payslip.employee.registration_number, 
            'full_name': _obj.payslip.employee.full_name(),
            'amount_qp_employee': abs(getattr(_obj, 'amount_qp_employee', 0)), 
            'amount_qp_employer': abs(getattr(_obj, 'amount_qp_employer', 0)),
            'obj': _obj
        } for _obj in ItemPaid.objects.filter(code=code, payslip__payroll=obj)]

        total = { field : round(sum([row.get(field, 0) for row in qs]), 2)
            for field in ['amount_qp_employee', 'amount_qp_employer']}
        return render(request, "payroll/listing.html", locals())
