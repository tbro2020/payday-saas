from django.utils.translation import gettext as _
from django.db import models

from core.utils import upload_directory_file
from core.models.fields import ModelSelect
from .employee import Employee
from core.models import Base


class Document(Base):
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    document = models.FileField(verbose_name=_('document'), upload_to=upload_directory_file)
    name = models.CharField(verbose_name=_('nom'), max_length=100)
    
    list_display = ('id', 'employee', 'name')
    inline_form_fields = ('document', 'name')

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
