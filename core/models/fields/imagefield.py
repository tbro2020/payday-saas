from django.db import models

class ImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.inline = kwargs.pop('inline', False)
        self.approver = kwargs.pop('approver', False)
        super().__init__(*args, **kwargs)