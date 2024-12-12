from core.models import Job, JobFrequencyChoice
from celery import shared_task

@shared_task(name='monthly')
def monthly():
    qs = Job.objects.filter(
        frequency=JobFrequencyChoice.MONTHLY,
    )
    for obj in qs:
        try:
            eval(obj.job, locals())
        except:
            pass
