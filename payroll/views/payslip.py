from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from core.forms import modelform_factory
from django.contrib import messages
from core.views import Change
from payroll import models

from core.models import Base

class Payslip(Change):
    template_name = "payroll/payslip.html"

    def get(self, request, pk):
        app, model = 'payroll', 'payslip'
        self.kwargs['app'] = app
        self.kwargs['model'] = model

        model = models.Payslip
        obj = get_object_or_404(model, pk=pk)
        items = obj.itempaid_set.all().order_by('code')

        form = modelform_factory(models.ItemPaid, fields='__all__')
        form = form()

        return render(request, self.template_name, locals())
    
    def post(self, request, pk):
        app, model = 'payroll', 'payslip'
        self.kwargs['app'] = app
        self.kwargs['model'] = model

        model = models.Payslip
        obj = get_object_or_404(model, pk=pk)

        base_fields = [field.name for field in Base._meta.fields] + ['id', 'payslip', 'rate', 'time']
        fields = [field.name for field in models.ItemPaid._meta.fields if field.name not in base_fields]

        form = modelform_factory(models.ItemPaid, fields=fields)
        form = form(request.POST)

        if not form.is_valid():
            messages.add_message(request, messages.WARNING, message=_(f'Remplissez correctement le formulaire'))
            return render(request, self.template_name, locals())

        instance = form.save(commit=False)

        instance.amount_qp_employee = abs(instance.amount_qp_employee) * instance.type_of_item
        instance.amount_qp_employer = abs(instance.amount_qp_employer)

        instance.social_security_amount = abs(instance.social_security_amount) * instance.type_of_item
        instance.taxable_amount = abs(instance.taxable_amount) * instance.type_of_item
        instance.is_payable = True
        instance.is_bonus = False # need to add field for this
        instance.payslip = obj
        instance.save()

        messages.add_message(request, messages.SUCCESS, message=_(f'L\'element a été ajouté avec succès'))
        return redirect(request.META.get('HTTP_REFERER'))