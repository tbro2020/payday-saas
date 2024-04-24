from core.utils import upload_directory_file
from .employee import Employee
from core.models import Base

from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from core.models.fields import DateField
from django.db import models


class Child(Base):
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    full_name = models.CharField(verbose_name=_('nom complet'), max_length=100)

    date_of_birth = DateField(verbose_name=_('date de naissance'))
    birth_certificate = models.FileField(verbose_name=_('certificat de naissance'), upload_to=upload_directory_file)

    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name', 'full_name') 
    inline_form_fields = ('full_name', 'date_of_birth', 'birth_certificate')
    list_display = ('id', 'employee', 'full_name', 'date_of_birth')

    @property
    def name(self):
        return self.full_name

    class Meta:
        verbose_name = _('enfant')
        verbose_name_plural = _('enfants')
