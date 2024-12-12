from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from payroll.models import Payroll
from payroll.tasks import Payer

@receiver(pre_save, sender=Payroll)
def payroll_create(sender, instance, **kwargs):
    if 'errors' in instance._metadata: return
    instance._metadata['errors'] = []

@receiver(post_save, sender=Payroll)
def payroll_created(sender, instance, created, **kwargs):
    if not created: return
    Payer().run(instance.id)
    #Payer().delay(instance.id)