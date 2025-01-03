from dal.autocomplete import TagSelect2
from django.db import models

class SelectListCreateChoiceField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = TagSelect2(attrs = {
            'data-minimum-input-length': 2,
            'data-theme': 'bootstrap-5'
        })
        return super().formfield(**kwargs)