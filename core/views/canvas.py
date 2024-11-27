from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from core.views import BaseView

import xlsxwriter
from io import BytesIO

class Canvas(BaseView):
    def get(self, request, pk):
        obj = get_object_or_404(ContentType, pk=pk)
        model = obj.model_class()

        fields = getattr(model, 'layout', None)
        if not fields:
            messages.error(request, 'Aucun layout n\'est défini pour ce modèle.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        fields = [field.name for field in fields.get_field_names()]
        fields = {field:model._meta.get_field(field) for field in fields 
                  if model._meta.get_field(field).get_internal_type() not in [
                      'FileField', 'ImageField', 'JSONField', 'BinaryField']}
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        for index, column in enumerate(fields.keys()):
            field = fields[column]
            worksheet.write(0, index, field.verbose_name.upper())
            
            if field.choices:
                worksheet.data_validation(1, index, 100000, index,  {
                    'validate': 'list',
                    'source': [choice[0] for choice in field.choices],
                    'input_title': 'Choose one:',
                    'input_message': 'Select a value from the list',
                })

            if field.is_relation or field.get_internal_type() in ['ForeignKey', 'OneToOneField', 'ModelSelect']:
                worksheet.data_validation(1, index, 100000, index,  {
                    'validate': 'list',
                    'source': [obj.name for obj in field.related_model.objects.all()],
                    'input_title': 'Choose one:',
                    'input_message': 'Select a value from the list',
                })
            
            if field.get_internal_type() in ['DateField', 'DateTimeField']:
                worksheet.data_validation(1, index, 100000, index,  {
                    'validate': 'date',
                    'criteria': 'between',
                    'minimum': '1900-01-01',
                    'maximum': '9999-12-31',
                    'input_title': 'Invalid date',
                    'input_message': 'Date must be between 1900-01-01 and 9999-12-31.',
                })

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(model._meta.verbose_name_plural)
        
        return response

