from crispy_forms.layout import Layout
from core.models import Base, fields

from django.utils.translation import gettext as _
from employee.models import Employee
from django.db import models

class Product(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100)

    class Meta:
        verbose_name = _('produit')
        verbose_name_plural = _('produits')

    search_fields = ('name',)
    list_display = ('id', 'name')
    layout = Layout('name', 'metadata')


class ProductRequest(Base):
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    description = fields.TextField(verbose_name=_('description'), blank=True)

    class Meta:
        verbose_name = _('demande de produit')
        verbose_name_plural = _('demandes de produits')

    search_fields = ('employee__matricule', ' employee__last_name', 'employee__first_name', 'description')
    list_display = ('id', 'employee', 'approved', 'created_at')
    inlines = ['logistic.productquantity',]
    
    layout = Layout('employee', 'description')
    _layout = Layout('employee', 'description')

    @property
    def name(self):
        return f"{self.employee} for {self.description}"


class ProductQuantity(Base):
    productrequest = fields.ForeignKey(ProductRequest, verbose_name=_('demande de produit #'), on_delete=models.CASCADE)
    product = fields.ModelSelectField(Product, verbose_name=_('produit'), on_delete=models.CASCADE, inline=True)
    requested_quantity = fields.FloatField(verbose_name=_('quantité demandée'), default=0.0, inline=True)

    observation = fields.CharField(verbose_name=_('observation'), max_length=250, blank=True, inline=True, approver=True)
    delivered_quantity = fields.FloatField(verbose_name=_('quantité livrée'), default=0.0, inline=True, approver=True)

    class Meta:
        verbose_name = _('quantité de produits')
        verbose_name_plural = _('quantités de produits')
    
    list_display = ('id', 'productrequest', 'product', 'quantity')
    layout = Layout('productrequest', 'product', 'quantity')
    search_fields = ('product__name',)

    @property
    def name(self):
        return f"{self.product} for {self.productrequest}"