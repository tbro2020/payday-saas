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
    menu.children.clear()
    menu.children.add(*content_types)