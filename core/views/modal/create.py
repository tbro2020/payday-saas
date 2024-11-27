from django.http import HttpResponse
from core.views.base import Create

class CreateModal(Create):
    next = HttpResponse(status=204, headers={'HX-Trigger': 'changed'})
    template_name = "modal/create.html"