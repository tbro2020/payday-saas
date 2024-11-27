from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from core.models import Approval

approved_signal = Signal()

@receiver(post_save, sender=Approval)
def saved(sender, instance, created, **kwargs):
    instance.object.approve()


