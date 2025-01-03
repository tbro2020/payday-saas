from core.models import Job
count = Job.objects.filter(is_active=True).count()