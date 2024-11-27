from django.shortcuts import render, redirect
from core.forms import InlineFormSetHelper
from django.contrib import messages
from .base import BaseView

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

class PasswordChange(BaseView):
    template_name = "registration/password_change.html"
    inline_formset_helper = InlineFormSetHelper()

    def get(self, request):
        model = get_user_model()
        obj = request.user
        
        form = PasswordChangeForm(obj, request.POST)
        return render(request, self.template_name, locals())
    
    def post(self, request):
        model = get_user_model()
        obj = request.user
        
        form = PasswordChangeForm(obj, request.POST)
        if not form.is_valid():
            messages.warning(request, _('veuillez remplir le formulaire correctement'))
            return render(request, self.template_name, locals())
        
        user = form.save()
        update_session_auth_hash(request, user)

        messages.success(request, _('votre mot de passe a été mis à jour avec succès'))
        return redirect("core:home")