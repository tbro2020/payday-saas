from django.core.validators import FileExtensionValidator
from django.db import models

from django import forms
from django.core.validators import FileExtensionValidator

class ImporterWidget(forms.ClearableFileInput):
    class Media:
        css = {
            'all': (
                'https://cdn.datatables.net/2.1.8/css/dataTables.bootstrap5.css'
            )
        }
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.js',
            'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/js/bootstrap.bundle.min.js',
            'https://cdn.datatables.net/2.1.8/js/dataTables.js',
            'https://cdn.datatables.net/2.1.8/js/dataTables.bootstrap5.js',
            'js/importer_widget.js'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'importer-widget'})

class ImporterField(models.FileField):
    default_validators = [FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])]

    def formfield(self, **kwargs):
        defaults = {'widget': ImporterWidget}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        self.validators = self.default_validators
        super().__init__(*args, **kwargs)

