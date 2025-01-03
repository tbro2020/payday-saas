from django.db import models
from django import forms

class DateField(models.DateField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = forms.DateInput(attrs={'class': 'datepicker'})
        return super().formfield(**kwargs)