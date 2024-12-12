from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def add_to_menu(sender, **kwargs):
    menu = apps.get_model("core", "menu")
    menu, created = menu.objects.get_or_create(icon="person-circle", name="employé")
    if created: print("Menu 'employé' créé")
    content_types = apps.get_model("contenttypes", "contenttype")
    content_types = content_types.objects.filter(app_label="employee").exclude(model__in=["child", "document"])
    if not menu.children.all().exists():
        menu.children.add(*content_types)
        print("Menu 'employé' mis à jour")

    defaults = {'value': '1'}
    preference = apps.get_model("core", "preference")
    preference.objects.get_or_create(key="CREATE_USER_ON_EMPLOYEE", defaults=defaults)
    preference.objects.get_or_create(key="DEFAULT_PERMISSION_GROUP", defaults=defaults)
