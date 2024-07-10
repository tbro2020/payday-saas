from dal.autocomplete import TagSelect2
from django.db import models


class SelectListCreateChoiceField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = TagSelect2(attrs = {
            'data-minimum-input-length': 2,
            'data-theme': 'bootstrap-5'
        })
        return super().formfield(**kwargs)