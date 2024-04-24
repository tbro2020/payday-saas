from django.db import models
from dal import autocomplete


class ChoiceField(models.CharField):
    def formfield(self, **kwargs):
        kwargs['widget'] = autocomplete.ListSelect2()
        return super().formfield(**kwargs)