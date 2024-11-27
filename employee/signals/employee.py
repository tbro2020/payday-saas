from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from employee.models import Employee
from core.models import Preference

User = get_user_model()

@receiver(post_save, sender=Employee)
def employee_created(sender, instance, created, **kwargs):
    # Early exit if not created or user creation is disabled
    if not created or not Preference.get('CREATE_USER_ON_EMPLOYEE', True):
        return
    
    # Create or update user with the employee's email
    user, _ = User.objects.get_or_create(
        email=instance.email,
        defaults={'employee': instance, 'is_active': True}
    )

    # Link employee if the user exists but isn't already linked
    if user.employee: return
    user.employee = instance
    user.save()