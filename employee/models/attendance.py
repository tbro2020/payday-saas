from core.models import Base, fields
from django.db import models

from django.utils.translation import gettext_lazy as _
from api.serializers import model_serializer_factory
from crispy_forms.layout import Layout, Row, Column


class Attendance(Base):
    DIRECTIONS = (
        ('IN', _('entrée')),
        ('OUT', _('sortie'))
    )

    employee = fields.ModelSelectField('employee.Employee', verbose_name=_('employé'), on_delete=models.CASCADE)
    direction = fields.CharField(_('direction'), max_length=10, choices=DIRECTIONS)
    
    time = fields.TimeField(verbose_name=_("heure"))
    date = fields.DateField(verbose_name=_("date"))

    list_display = ('id', 'employee', 'date', 'time', 'direction')
    list_filter = ('date', 'time', 'direction')

    layout = Layout(
        Row(
            Column('employee', css_class='form-group col-md-6 mb-0'),
            Column('direction', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'
        ),
        Row(
            Column('date', css_class='form-group col-md-6 mb-0'),
            Column('time', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'
        ),
    )

    @property
    def name(self):
        return "{} at {}".format(self.employee, self.date)
    
    def json(self):
        serializer = model_serializer_factory(self._meta.model, depth=1)
        return serializer(self).data

    class Meta:
        verbose_name = _("présence")
        verbose_name_plural = _("présences")
        unique_together = ('employee', 'date', 'direction')