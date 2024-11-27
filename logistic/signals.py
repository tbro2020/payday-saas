from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from logistic.models import *

@receiver(post_save, sender=LabourRequest)
def labour_request_approved(sender, instance, created, **kwargs):
    if created: return

@receiver(post_save, sender=ProductRequest)
def product_request_approved(sender, instance, created, **kwargs):
    if created: return

@receiver(post_save, sender=VehicleRequest)
def vehicle_request_approved(sender, instance, created, **kwargs):
    if created: return
