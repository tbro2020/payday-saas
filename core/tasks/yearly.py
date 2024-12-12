from core.models import Job, JobFrequencyChoice
from celery import shared_task

@shared_task(name='yearly')
def yearly():
    qs = Job.objects.filter(
        frequency=JobFrequencyChoice.YEARLY,
    )
    for obj in qs:
        try:
            eval(obj.job, locals())
        except:
            pass
