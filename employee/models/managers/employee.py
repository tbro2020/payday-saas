from core.models.managers import QuerySet
from django.utils import timezone
from django.db.models import Q

class EmployeeQuerySet(QuerySet):
    def retired_on(self, period):
        return self.all()
    
    def leave_on(self, period):
        return self.all()