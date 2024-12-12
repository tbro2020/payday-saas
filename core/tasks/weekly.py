from core.models import Job, JobFrequencyChoice
from celery import shared_task

@shared_task(name='weekly')
def weekly():
    qs = Job.objects.filter(
        frequency=JobFrequencyChoice.WEEKLY,
    )
    for obj in qs:
        try:
            eval(obj.job, locals())
        except:
            pass
