from django.http import HttpResponse
from core.views.base import Change

class ChangeModal(Change):
    next = HttpResponse(status=204, headers={'HX-Trigger': 'changed'})
    template_name = "modal/change.html"