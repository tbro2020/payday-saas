from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

from core.forms import modelform_factory
from core.forms import UserCreationForm
from core.models import Organization

class CreateOrganization(View):
    template_name = "organization.html"

    def get(self, request):
        organization = modelform_factory(Organization, fields=['logo', 'name'])
        user = UserCreationForm()
        return render(request, self.template_name, locals())
    
    def post(self, request):
        organization = modelform_factory(Organization, fields=['logo', 'name'])
        organization = organization(request.POST, request.FILES or None)
        if not organization.is_valid():
            messages.error(request, _("Veuillez remplir correctement le formulaire"))
            return render(request, self.template_name, locals())
        # organization.save()
        user = UserCreationForm(request.POST, request.FILES or None)
        if not user.is_valid():
            messages.error(request, _("Veuillez remplir correctement le formulaire"))
            return render(request, self.template_name, locals())
        
        user = user.save(commit=False)
        organization.save()
        
        user.organization = organization.instance
        user.is_superuser = True
        user.save()

        messages.success(request, _("Votre organisation a été créée avec succès"))
        return redirect(reverse_lazy('login'))