from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from django import forms

class InlineForm(forms.Form):
    class Meta:
        fields = '__all__'

    def __init__(self, args, kwargs):
        super(InlineForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
