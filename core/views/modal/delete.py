from django.http import HttpResponse
from core.views.base import Delete

class DeleteModal(Delete):
    next = HttpResponse(status=204, headers={'HX-Trigger': 'changed'})
    template_name = "modal/delete.html"