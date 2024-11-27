from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.apps import apps

class OrganizationMiddleware:
    organization_path = reverse_lazy('core:create-organization')

    def __init__(self, get_response):
        self.get_response = get_response
    
    def organization(self):
        model = apps.get_model('core.organization')
        return model.objects.all().first()

    def __call__(self, request):
        path = request.path
        organization = self.organization()
        request.organization = organization
        
        if organization == None and path != self.organization_path:
            return redirect(reverse_lazy('core:create-organization')+"?next="+path)
        return self.get_response(request)