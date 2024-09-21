from django_json_widget.widgets import JSONEditorWidget
from django.db import models


class JSONField(models.JSONField):
    def formfield(self, **kwargs):
        kwargs['widget'] = JSONEditorWidget(width='100%', height='400px', options={
            'mode': 'tree'
        })
        return super().formfield(**kwargs)