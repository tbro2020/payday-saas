from core.utils import upload_directory_file
from .employee import Employee
from core.models import Base

from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from core.models.fields import DateField
from django.db import models


class Education(Base):
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    
    institution = models.CharField(_('institution'), max_length=100, blank=True, null=True, default=None)
    degree = models.CharField(_('diplôme'), max_length=100, blank=True, null=True, default=None)
    
    start_date = DateField(_('date de début'), null=True, default=None)
    end_date = DateField(_('date de fin'), null=True, default=None)
    
    photo = models.ImageField(_('photo'), upload_to=upload_directory_file, blank=True, null=True, default=None)

    list_display = ['employee', 'institution', 'degree', 'start_date', 'end_date']
    inline_form_fields = ['institution', 'degree', 'start_date', 'end_date', 'photo']

    @property
    def name(self):
        return "%s de %s" % (self.degree, self.employee.name)

    class Meta:
        verbose_name = _('education')
        verbose_name_plural = _('educations')
