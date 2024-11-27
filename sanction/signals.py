from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from sanction.models import *

@receiver(post_save, sender=Sanction)
def sanction_approved(sender, instance, created, **kwargs):
    if created: return
