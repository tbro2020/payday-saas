from django.utils.translation import gettext as _
from django_ace import AceWidget
from django.db import models
from typing import Any

class CustomAceWidget(AceWidget):
    pass

class AceField(models.TextField):

    def __init__(self, mode='python', *args: Any, **kwargs: Any) -> None:
        self.mode = mode
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        

        help_text =_(
            'press "Ctrl+Space" to get code completion'
            'press "Ctrl+M" to toggle in modal mode'
        )
        kwargs['help_text'] = kwargs.get('help_text', help_text)
        
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = CustomAceWidget(**{
            'mode': self.mode,
            'theme': 'twilight',
            'width': '100% !important',
            # 'height': '150px !important',
            'showprintmargin': False,
            'toolbar': True,
            'showgutter': True,
            'behaviours': True,
        })
        return super().formfield(**kwargs)