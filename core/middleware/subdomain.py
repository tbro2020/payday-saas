from django.contrib.auth import logout
from django.shortcuts import redirect
from core.models import Organization
from django.urls import reverse_lazy

class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def hostname_from_request(self, request):
        # split on `:` to remove port
        return request.get_host().split(':')[0].lower()
    
    def subdomain(self, request):
        hostname = self.hostname_from_request(request)
        return hostname.split('.')[0]
    
    def organization(self, subdomain):
        return Organization.objects.filter(subdomain_prefix=subdomain).first()

    def __call__(self, request):
        request.subdomain = self.subdomain(request)
        request.organization = self.organization(request.subdomain)

        # if non sub domain redirect to the page of create new organization
        if request.organization == None and request.path != reverse_lazy('core:create-organization'):
            return redirect(reverse_lazy('core:create-organization')+"?next="+request.path)

        return self.get_response(request)
