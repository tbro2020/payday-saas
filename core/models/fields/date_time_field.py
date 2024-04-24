from django.db import models
from django import forms


class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        kwargs['widget'] = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return super().formfield(**kwargs)