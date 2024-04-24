from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from employee.models import Employee
from core.models import Preference

User = get_user_model()

@receiver(post_save, sender=Employee)
def employee_created(sender, instance, created, **kwargs):
    if not created: return
    can_create_employee = Preference.get('CREATE_USER_ON_EMPLOYEE')
    if not can_create_employee: return

    if user := User.objects.filter(email=instance.email).first():
        if user.employee: return
        user.employee = instance
        return user.save()

    obj, created = User.objects.get_or_create(**{
        'email': instance.email,
        'employee': instance,
        'is_active': True
    })
    if not created: return
