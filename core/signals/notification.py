from django.db.models.signals import post_save
from core.models import Notification
from django.dispatch import receiver


@receiver(post_save, sender=Notification)
def saved(sender, instance, created, **kwargs):
    if not created: return
    try:
        instance._to.email_user(instance._subject, instance._message)
    except Exception as ex:
        print(ex)