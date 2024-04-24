from django.db import models
from django import forms


class TimeField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = forms.TimeInput(attrs={'type': 'time'})
        return super().formfield(**kwargs)