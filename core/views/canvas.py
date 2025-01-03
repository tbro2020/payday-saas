from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.contrib import messages
from core.views import BaseView

import xlsxwriter
from io import BytesIO

class Canvas(BaseView):
    MAX_ROWS = 200
    NUMBER_RANGE = (0, 999999999)
    DATE_RANGE = ('1900-01-01', '2100-12-31')
    EXCLUDED_FIELDS = [
        'organization', 
        'created_by', 
        'updated_by', 
        'created_at', 
        'updated_at', 
        '_metadata'
    ]
    EXCLUDED_FIELD_TYPES = [
        'AutoField', 
        'BigAutoField',
        'ManyToManyField',
        'ImageField',
        'FileField',
        'ImporterField'
    ]
    

    def get(self, request, pk):
        obj = get_object_or_404(ContentType, pk=pk)
        model = obj.model_class()

        fields = self._get_model_fields(model)
        if not fields:
            messages.error(request, _("Aucun layout n'est défini pour ce modèle."))
            return redirect(request.META.get('HTTP_REFERER'))
        
        output = self._generate_excel(fields, model)
        
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={model._meta.verbose_name_plural}.xlsx"
        return response

    def _get_model_fields(self, model):
        fields = getattr(model, 'layout', None)
        if not fields:
            return None
        
        field_names = [field.name for field in fields.get_field_names()]
        fields = {field: model._meta.get_field(field) for field in field_names}
        
        for field in self.EXCLUDED_FIELDS:
            fields.pop(field, None)
        
        return fields
    
    def _generate_excel(self, fields, model):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        for index, (column, field) in enumerate(fields.items()):
            worksheet.write(0, index, field.verbose_name.upper())
            self._apply_data_validation(worksheet, index, field)
        
        workbook.close()
        output.seek(0)
        return output
    
    def _is_single_relation_field(self, field):
        if field.is_relation and hasattr(field, 'remote_field') and field.remote_field:
            return True
        return False
    

    def _apply_data_validation(self, worksheet, index, field):
        if field.choices:
            worksheet.data_validation(1, index, self.MAX_ROWS, index, {
                'validate': 'list',
                'source': [choice[0] for choice in field.choices],
                'input_title': 'Choose one:',
                'input_message': _('Select a value from the list'),
            })

        elif self._is_single_relation_field(field):
            worksheet.data_validation(1, index, self.MAX_ROWS, index, {
                'validate': 'list',
                'source': [obj.name for obj in field.related_model.objects.all()],
                'input_title': 'Choose one:',
                'input_message': _('Select a value from the list'),
            })

        elif field.get_internal_type() in ['DateField', 'DateTimeField']:
            worksheet.data_validation(1, index, self.MAX_ROWS, index, {
                'validate': 'date',
                'criteria': 'between',
                'minimum': self.DATE_RANGE[0],
                'maximum': self.DATE_RANGE[1],
                'input_title': 'Invalid date',
                'input_message': _('Date must be between {0} and {1}.').format(*self.DATE_RANGE),
            })

        elif field.get_internal_type() in ['IntegerField', 'DecimalField', 'FloatField']:
            worksheet.data_validation(1, index, self.MAX_ROWS, index, {
                'validate': 'integer',
                'criteria': 'between',
                'minimum': self.NUMBER_RANGE[0],
                'maximum': self.NUMBER_RANGE[1],
                'input_title': 'Invalid number',
                'input_message': _('Number must be between {0} and {1}.').format(*self.NUMBER_RANGE),
            })
