from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def add_to_menu(sender, **kwargs):
    menu = apps.get_model("core", "menu")
    menu, created = menu.objects.get_or_create(icon="cash", name="paie")
    if created: print("Menu 'payroll' créé")
    content_types = apps.get_model("contenttypes", "contenttype")
    content_types = content_types.objects.filter(app_label="payroll").exclude(model__in=[
        "itempaid", "paidemployee", "specialemployeeitem", "advancesalarypayment"
    ])
    if menu.children.all().exists(): return
    menu.children.add(*content_types)
    print("Menu 'payroll' mis à jour")