from django_json_widget.widgets import JSONEditorWidget
from django.db import models

class JSONField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = JSONEditorWidget(width='100%', height='400px', options=dict(mode='tree'))
        return super().formfield(**kwargs)