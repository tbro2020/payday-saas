from django.utils.translation import gettext as _
from employee.models import *
from django_filters import *
from django import forms

from django.db.models import Q
from functools import reduce

class PayslipFilter(FilterSet):
    q = CharFilter(label=str, method='search', widget=forms.TextInput(attrs={'class': 'form-control d-none'}))
    status = ChoiceFilter(label=_('Status'), method='by_status', choices=Status.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'}))
    branch = ChoiceFilter(label=_('Site'), method='by_branch', choices=Branch.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'})) 
    payer = ChoiceFilter(label=_('Banque'), method='by_payer', choices=Payer.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'}))
    grade = ChoiceFilter(label=_('Grade'), method='by_grade', choices=Grade.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'}))

    def search(self, queryset, name, value):
        fields = ['_employee__registration_number', '_employee__middle_name', '_employee__last_name']
        query = reduce(lambda q, field: q | Q(**{f"{field}__icontains": value}), fields, Q())
        return queryset.filter(query).distinct()

    def by_branch(self, queryset, name, value):
        return queryset.filter(_employee__branch__name=value)
    
    def by_grade(self, queryset, name, value):
        return queryset.filter(_employee__grade__name=value)

    def by_payer(self, queryset, name, value):
        return queryset.filter(payer__name=value)
    
    def by_status(self, queryset, name, value):
        return queryset.filter(_employee__status__name=value)

    class Meta:
        fields = ('branch', 'grade', 'payer', 'status')