from core.models import Job, JobFrequencyChoice
from celery import shared_task

@shared_task(name='hourly')
def hourly():
    qs = Job.objects.filter(
        frequency=JobFrequencyChoice.HOURLY,
    )
    for obj in qs:
        try:
            eval(obj.job, locals())
        except:
            pass
