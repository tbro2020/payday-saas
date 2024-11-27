from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models import Base, fields
from django.db import models

from employee.models import Employee
from datetime import datetime

class VehicleRequest(Base):
    destination = fields.CharField(verbose_name=_('destination'), max_length=250, null=True, default=None)
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    leaving_time = fields.TimeField(verbose_name=_('heure de départ'), default=datetime.today)
    reason = fields.TextField(verbose_name=_('raison'))
    
    vehicle_licence_plate = fields.CharField(verbose_name=_('plaque d\'immatriculation du véhicule'), max_length=250, null=True, default=None, approver=True)
    type_of_vehicle = fields.CharField(verbose_name=_('type de véhicule'), max_length=250, null=True, default=None, approver=True)
    driver_name = fields.CharField(verbose_name=_('nom du conducteur'), max_length=250, null=True, default=None, approver=True)

    class Meta:
        verbose_name = _('demande de véhicule')
        verbose_name_plural = _('demandes de véhicules')

    search_fields = ('employee__matricule', ' employee__last_name', 'employee__first_name', 'reason', 'destination', 'type_of_vehicle', 'driver_name', 'vehicle_licence_plate')
    list_display = ('id', 'employee', 'leaving_time', 'destination', 'approved', 'updated_on')
    list_filter = ('updated_at',)
    layout = Layout(
        'employee',
        Row(Column('destination'), Column('leaving_time')),
        Row(Column('type_of_vehicle'),Column('driver_name'),Column('vehicle_licence_plate')),
        'reason'
    )

    @property
    def name(self):
        return f"{self.employee}"