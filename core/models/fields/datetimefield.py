from django.db import models
from django import forms

class DateTimeField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return super().formfield(**kwargs)