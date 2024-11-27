from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Approval

@receiver(post_save, sender=Approval)
def saved(sender, instance, created, **kwargs):
    instance.object.approve()


