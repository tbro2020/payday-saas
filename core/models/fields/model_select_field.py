from django.urls import reverse_lazy
from django.db import models
from dal import autocomplete

class ModelSelectField(models.ForeignKey):
    on_delete = models.SET_NULL
    default = None
    null = True

    def __init__(self, *args, **kwargs):
        self.on_delete = kwargs.pop('on_delete', self.on_delete)
        self.default = kwargs.pop('default', self.default)
        self.null = kwargs.pop('null', self.null)
        self.inline = kwargs.pop('inline', False)
        self.level = kwargs.pop('level', 0)

        super().__init__(null=self.null, on_delete=self.on_delete, default=self.default, *args, **kwargs)
    
    def formfield(self, **kwargs):
        to_field = getattr(self, 'foreign_related_fields', None)
        to_field = to_field[0].name if to_field else 'pk'
        kwargs['widget'] = autocomplete.ModelSelect2(url=reverse_lazy('api:autocomplete', kwargs={
            'to_field': to_field,
            'app': self.remote_field.model._meta.app_label,
            'model': self.remote_field.model._meta.model_name
        }), attrs = {
            'data-minimum-input-length': 2,
            'data-theme': 'bootstrap-5'
        })
        return super().formfield(**kwargs)