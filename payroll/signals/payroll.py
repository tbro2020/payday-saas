from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache

from payroll.models import Payroll
from payroll.tasks import Payer

@receiver(pre_save, sender=Payroll)
def payroll_create(sender, instance, **kwargs):
    if 'errors' in instance.metadata: return
    instance.metadata['errors'] = []

@receiver(post_save, sender=Payroll)
def payroll_created(sender, instance, created, **kwargs):
    if not created: return
    task_id = Payer().delay(instance.id).id
    cache.set(f'payroll_{instance.id}', task_id, timeout=None)