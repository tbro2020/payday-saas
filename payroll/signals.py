from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.apps import apps

from payroll.payer import Payer
from payroll.models import *


payer = Payer()

@receiver(pre_save, sender=Payroll)
def payroll_create(sender, instance, **kwargs):
    if 'errors' in instance.metadata: return
    instance.metadata['errors'] = []

@receiver(post_save, sender=Payroll)
def payroll_created(sender, instance, created, **kwargs):
    if not created: return
    payer.delay(instance.pk)

"""   
@receiver(post_delete, sender=Payslip)
def payslip_deleted(sender, instance, **kwargs):
    return
    #try:
    #    overall_net = instance.payroll.payslip_set.all().aggregate(amount=Sum('net')).get('amount', 0)
    #    instance.payroll.overall_net = round(overall_net, 2) if overall_net else 0
    #    instance.payroll.save()
    #except Exception as ex:
    #    pass
    
@receiver(post_delete, sender=PayItem)
def pay_item_deleted(sender, instance, **kwargs):
    return
    #payer.run(instance.payslip.payroll, employee={'pk': instance.payslip.employee.id})
    #payer.delay(instance.payslip.payroll.id, employee={'pk': instance.payslip.employee.id})
"""