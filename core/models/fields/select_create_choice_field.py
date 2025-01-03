from django.db import models
from dal import autocomplete

class SelectCreateChoiceField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**kwargs)
    