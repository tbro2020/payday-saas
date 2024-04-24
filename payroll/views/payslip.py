from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from core.forms import modelform_factory
from django.contrib import messages
from core.views import BaseView
from payroll.payer import Payer
from payroll import models



class Payslip(BaseView):
    payer = Payer()
    
    def get(self, request, pk):
        payslip = models.Payslip
        obj = get_object_or_404(payslip, pk=pk)
        items = obj.payitem_set.all().order_by('code')

        form = modelform_factory(models.PayItem, fields='__all__')
        form = form()

        return render(request, 'payroll/payslip.html', locals())
    
    def post(self, request, pk):
        payslip = models.Payslip
        obj = get_object_or_404(payslip, pk=pk)
        items = obj.payitem_set.all().order_by('code')

        fields = ['type_of_item', 'code', 'name', 'amount', 'taxable_amount', 'social_security_amount']
        form = modelform_factory(models.PayItem, fields=fields)
        form = form(request.POST)

        if not form.is_valid():
            messages.add_message(request, messages.WARNING, message=_(f'Remplissez correctement le formulaire'))
            return render(request, 'payroll/payslip.html', locals())

        instance = form.save(commit=False)
        instance.amount = abs(instance.amount) * instance.type_of_item
        instance.taxable_amount = abs(instance.taxable_amount) * instance.type_of_item
        instance.social_security_amount = abs(instance.social_security_amount) * instance.type_of_item
        instance.payslip = obj
        instance.save()

        messages.add_message(request, messages.SUCCESS, message=_(f'L\'element a été ajouté avec succès'))
        self.payer.delay(obj.payroll.id, employee={'pk': obj.employee.id})
        return redirect(request.META.get('HTTP_REFERER'))