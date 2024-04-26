from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper


class InlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'