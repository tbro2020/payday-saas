from django.db import models

class PositiveBigIntegerField(models.PositiveBigIntegerField):
    def __init__(self, *args, **kwargs):
        self.inline = kwargs.pop('inline', False)
        self.approver = kwargs.pop('approver', False)
        super().__init__(*args, **kwargs)
