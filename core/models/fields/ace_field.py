from django.utils.translation import gettext as _
from django_ace import AceWidget
from django.db import models
from typing import Any


class AceField(models.TextField):

    def __init__(self, mode='python', *args: Any, **kwargs: Any) -> None:
        self.mode = mode
        self.inline = kwargs.pop('inline', False)
        self.approver = kwargs.pop('approver', False)

        help_text =_('press "Ctrl+Space" to get code completion')
        kwargs['help_text'] = kwargs.get('help_text', help_text)
        
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
            'behaviours': True,
        })
        return super().formfield(**kwargs)