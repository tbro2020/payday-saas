from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from payroll.models import ItemPaid
from payroll.tasks import Payer

from django.db.models import Sum

payer = Payer()

@receiver(post_save, sender=ItemPaid)
def item_paid_created(sender, instance, created, **kwargs):
    if not created: return
    payroll = instance.payslip.payroll
    employee = instance.payslip.employee
    payer.run(payroll.id, employee={
        employee._meta.pk.name: getattr(employee, employee._meta.pk.name, None)
    })

@receiver(post_delete, sender=ItemPaid)
def item_paid_deleted(sender, instance, **kwargs):
    try:
        payroll = instance.payslip.payroll
        employee = instance.payslip.employee
        payer.run(payroll.id, employee={employee._meta.pk.name: getattr(employee, employee._meta.pk.name, None)})
    except Exception as ex:
        print(ex)