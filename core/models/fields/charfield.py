from django.db import models
from django import forms

class CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)

    """
    def formfield(self, **kwargs):
        kwargs['widget'] = forms.TextInput(attrs={
            'readonly': 'readonly',
            #'class': 'form-control-plaintext',
        })
        return super().formfield(**kwargs)
    """
