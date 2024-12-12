from core.models import Job, JobFrequencyChoice
from celery import shared_task

@shared_task(name='daily')
def daily():
    qs = Job.objects.filter(
        frequency=JobFrequencyChoice.DAILY,
    )
    for obj in qs:
        try:
            eval(obj.job, locals())
        except:
            pass
