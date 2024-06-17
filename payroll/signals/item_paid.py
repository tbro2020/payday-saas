from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from payroll.models import ItemPaid
from payroll.tasks import Payer

def refresh(instance):
    try:
        payroll = instance.payslip.payroll
        employee = instance.payslip.employee
        Payer().run(payroll.id, employee={'registration_number': employee.registration_number})
    except Exception as ex:
        print(ex)

@receiver(post_save, sender=ItemPaid)
def item_paid_created(sender, instance, created, **kwargs):
    if not created: return
    refresh(instance)

@receiver(post_delete, sender=ItemPaid)
def item_paid_deleted(sender, instance, **kwargs):
    refresh(instance)