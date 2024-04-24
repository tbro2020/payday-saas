from dal.autocomplete import TagSelect2
from django.db import models
from dal import autocomplete


class SelectListCreateChoiceField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = TagSelect2()
        return super().formfield(**kwargs)