from typing import Any
from django_ace import AceWidget
from django.db import models


class AceField(models.TextField):

    def __init__(self, mode='python', *args: Any, **kwargs: Any) -> None:
        self.mode = mode
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = AceWidget(mode=self.mode, theme='dracula', width='100% !important', toolbar=False, showgutter=False)
        return super().formfield(**kwargs)