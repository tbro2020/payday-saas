from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models import Base, fields

from sanction.models.type_of_sanction import TypeOfSanction
from employee.models import Employee
from django.db import models

class Sanction(Base):
    type_of_sanction = fields.ModelSelectField(TypeOfSanction, verbose_name=_('type de sanction'), on_delete=models.CASCADE)
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    description = fields.TextField(verbose_name=_('description'))

    start_dt = fields.DateField(verbose_name=_('date de debut'))
    end_dt = fields.DateField(verbose_name=_('date de fin'))

    class Meta:
        verbose_name = _('sanction')
        verbose_name_plural = _('sanctions')

    search_fields = ('type_of_sanction__name', 'employee__matricule', ' employee__last_name', 'employee__first_name')
    list_display = ('id', 'type_of_sanction', 'employee', 'approved', 'updated_at')
    list_filter = ('type_of_sanction', 'updated_at')
    
    layout = Layout(
        Row(Column('type_of_sanction'), Column('employee')),
        Row(Column('start_dt'), Column('end_dt')),
        'description'
    )

    @property
    def name(self):
        return f"{self.type_of_sanction} for {self.employee}"
