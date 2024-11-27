from django.db import models
from django import forms

class TimeField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.inline = kwargs.pop('inline', False)
        self.approver = kwargs.pop('approver', False)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = forms.TimeInput(attrs={'type': 'time'})
        return super().formfield(**kwargs)