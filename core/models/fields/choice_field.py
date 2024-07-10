from django.db import models
from dal import autocomplete


class ChoiceField(models.CharField):
    def formfield(self, **kwargs):
        kwargs['widget'] = autocomplete.ListSelect2(attrs = {
            'data-minimum-input-length': 2,
            'data-theme': 'bootstrap-5'
        })
        return super().formfield(**kwargs)