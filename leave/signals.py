from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from leave.models import *

@receiver(post_save, sender=Leave)
def leave_approved(sender, instance, created, **kwargs):
    if created: return


@receiver(post_save, sender=EarlyLeave)
def early_leave_approved(sender, instance, created, **kwargs):
    if created: return
