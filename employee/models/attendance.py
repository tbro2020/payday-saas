from core.models.fields import ModelSelect
from django.db import models
from core.models import Base

from django.utils.translation import gettext_lazy as _
from api.serializers import model_serializer_factory
from crispy_forms.layout import Layout, Row, Column
from core.models.fields import DateField, TimeField


class Attendance(Base):
    DIRECTIONS = (
        ('IN', _('entrée')),
        ('OUT', _('sortie'))
    )

    employee = ModelSelect('employee.Employee', verbose_name=_('employé'), on_delete=models.CASCADE)
    direction = models.CharField(_('direction'), max_length=10, choices=DIRECTIONS)
    date = DateField(verbose_name=_("date"))
    time = TimeField(verbose_name=_("heure"))

    list_display = ('id', 'employee', 'date', 'time', 'direction')
    list_filter = ('date', 'time', 'direction')

    layout = Layout(
        Row(
            Column('employee', css_class='form-group col-md-6 col-sm-12 mb-0'),
            Column('direction', css_class='form-group col-md-6 col-sm-12 mb-0'),
            css_class='form-row'
        ),
        Row(
            Column('date', css_class='form-group col-md-6 col-sm-12 mb-0'),
            Column('time', css_class='form-group col-md-6 col-sm-12 mb-0'),
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