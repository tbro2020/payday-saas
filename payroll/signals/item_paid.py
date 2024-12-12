from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from payroll.models import ItemPaid, Payslip, Payroll
from django.db.models import Sum

def refresh(instance):
    #try:
    #    payroll = instance.payslip.payroll
    #    employee = instance.payslip.employee
    #    Payer().run(payroll.id, employee={'registration_number': employee.registration_number})
    #except Exception as ex:
    #    print(ex)

    items_paid = ItemPaid.objects.filter(payslip=instance.payslip, is_payable=True)
    social_security_amount = round(items_paid.aggregate(amount=Sum('social_security_amount'))['amount'] or 0, 2)
    amount_qp_employee = round(items_paid.aggregate(amount=Sum('amount_qp_employee'))['amount'] or 0, 2)
    taxable_amount = round(items_paid.aggregate(amount=Sum('taxable_amount'))['amount'] or 0, 2)

    Payslip.objects.filter(pk=instance.payslip.pk).update(**{
        'social_security_threshold': social_security_amount,
        'taxable_gross': taxable_amount,
        'gross': amount_qp_employee,
        'net': amount_qp_employee
    })

    net = instance.payslip.payroll.payslip_set.aggregate(amount=Sum('net')).get('amount', 0)
    net = round(net, 2) if net else 0

    Payroll.objects.filter(pk=instance.payslip.payroll.pk).update(**{
        'overall_net': net
    })

@receiver(post_save, sender=ItemPaid)
def item_paid_created(sender, instance, created, **kwargs):
    if not created: return
    refresh(instance)

@receiver(post_delete, sender=ItemPaid)
def item_paid_deleted(sender, instance, **kwargs):
    try:
        refresh(instance)
    except Exception as ex:
        print(ex)