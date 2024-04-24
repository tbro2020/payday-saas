from django.db import models
from datetime import date
from django import forms



class DateField(models.DateField):
    def formfield(self, **kwargs):
        today = date.today()
        kwargs['widget'] = forms.DateInput(attrs={'class': 'datepicker'})
        return super().formfield(**kwargs)