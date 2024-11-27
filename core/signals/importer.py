from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Importer
from core.tasks import importer

@receiver(post_save, sender=Importer)
def saved(sender, instance, created, **kwargs):
    if not created: return
    importer.delay(instance.pk)