from django.db.models.signals import post_save
from django.dispatch import receiver

from payroll.models import AdvanceSalary, AdvanceSalaryPayment
from datetime import timedelta

@receiver(post_save, sender=AdvanceSalary)
def saved(sender, instance, created, **kwargs):
    if not created: return
    amount = instance.amount / instance.duration
    advance_salary_payments = [AdvanceSalaryPayment(
        advance_salary=instance,
        amount=amount,
        date=instance.date + timedelta(days=30*(i + 1))
    ) for i in range(instance.duration)]
    AdvanceSalaryPayment.objects.bulk_create(advance_salary_payments)