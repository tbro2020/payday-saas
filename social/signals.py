from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from social.models import *

@receiver(post_save, sender=FundRequest)
def fund_request_approved(sender, instance, created, **kwargs):
    if created: return
