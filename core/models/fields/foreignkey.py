from django.db import models

class ForeignKey(models.ForeignKey):
    on_delete = models.SET_NULL
    default = None
    null = True

    def __init__(self, *args, **kwargs):
        self.on_delete = kwargs.pop('on_delete', self.on_delete)
        self.default = kwargs.pop('default', self.default)
        self.null = kwargs.pop('null', self.null)
        self.level = kwargs.pop('level', 0)
        
        
        self.inline = kwargs.pop('inline', False)

        super().__init__(null=self.null, on_delete=self.on_delete, default=self.default, *args, **kwargs)
