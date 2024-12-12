from django.utils.translation import gettext as _
from employee.models import *
from django_filters import *
from django import forms

from django.db.models import Q
from functools import reduce

class PayslipFilter(FilterSet):
    status = ChoiceFilter(label=_('Status'), method='by_status', choices=Status.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'}))
    branch = ChoiceFilter(label=_('Site'), method='by_branch', choices=Branch.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'})) 
    grade = ChoiceFilter(label=_('Grade'), method='by_grade', choices=Grade.objects.values_list('name', 'name').distinct(), widget=forms.Select(attrs={'class': 'form-control'}))
    q = CharFilter(label=str, method='search', widget=forms.TextInput(attrs={'class': 'form-control d-none'}))

    def search(self, queryset, name, value):
        fields = ['employee__registration_number', 'employee__middle_name', 'employee__last_name']
        query = reduce(lambda q, field: q | Q(**{f"{field}__icontains": value}), fields, Q())
        return queryset.filter(query).distinct()

    def by_branch(self, queryset, name, value):
        return queryset.filter(employee__branch__name=value)
    
    def by_grade(self, queryset, name, value):
        return queryset.filter(employee__grade__name=value)
    
    def by_status(self, queryset, name, value):
        return queryset.filter(employee__status__name=value)

    class Meta:
        fields = ('branch', 'grade', 'status')