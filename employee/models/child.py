from core.utils import upload_directory_file
from crispy_forms.layout import Layout
from core.models import Base, fields
from .employee import Employee

from django.utils.translation import gettext as _
from django.db import models


class Child(Base):
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    full_name = fields.CharField(verbose_name=_('nom complet'), max_length=100, inline=True)

    birth_certificate = fields.FileField(verbose_name=_('certificat de naissance'), upload_to=upload_directory_file, inline=True)
    date_of_birth = fields.DateField(verbose_name=_('date de naissance'), inline=True)

    list_display = ('id', 'employee', 'full_name', 'date_of_birth')
    search_fields = ('employee__registration_number', 'full_name') 
    layout = Layout(
        'full_name',
        'birth_certificate',
        'date_of_birth',
    )

    @property
    def name(self):
        return self.full_name

    class Meta:
        verbose_name = _('enfant')
        verbose_name_plural = _('enfants')
