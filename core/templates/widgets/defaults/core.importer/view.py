from core.models import Importer, ImporterStatus

count = Importer.objects.filter(status=ImporterStatus.PENDING).count()