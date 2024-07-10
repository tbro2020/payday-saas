from typing import Any
from django_ace import AceWidget
from django.db import models


class AceField(models.TextField):

    def __init__(self, mode='python', *args: Any, **kwargs: Any) -> None:
        self.mode = mode
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        
        kwargs['widget'] = AceWidget(**{
            'mode': self.mode,
            'theme': 'twilight',
            'width': '100% !important',
            'height': '150px !important',
            'showprintmargin': False,
            'toolbar': False,
            'showgutter': True,
            'behaviours': True
        })
        return super().formfield(**kwargs)