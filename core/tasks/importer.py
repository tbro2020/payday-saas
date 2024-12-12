from core.models import ImporterStatus, Notification
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from django.template import loader
from celery import shared_task
from django.apps import apps
import pandas as pd


@shared_task(name='importer')
def importer(pk):
    model = apps.get_model('core', 'importer')
    obj = model.objects.get(pk=pk)

    # Check if user has permission to add
    permission = '{}.add_{}'.format(obj.content_type.app_label, obj.content_type.model)
    
    if not obj.created_by.has_perm(permission):
        obj.message = _('Vous n\'avez pas la permission d\'ajouter des données')
        obj.status = ImporterStatus.ERROR
        obj.save()

        try:
            return obj.created_by.email_user(**{
                'subject': _(f'Importation a échoué'),
                'message': loader.render_to_string('email/importation_failed.txt')
            })
        except:
            print('Email not sent')
            return

    # Update status
    obj.status = ImporterStatus.PROCESSING
    obj.save()

    # Get model
    model = obj.content_type.model_class()
    fields = {field.verbose_name:field for field in model._meta.fields}
    
    # Read excel file
    df = pd.read_excel(obj.document, dtype=str)
    df = df.where(pd.notnull(df), None)
    df.columns = [fields[col.lower()].name for col in df.columns]
    fields = {field.name:field.related_model.objects.values('id', 'name') 
            for field in fields.values() if field.is_relation and field.name in df.columns}

    try:
        data = df.to_dict(orient='records')
        [row.update({'created_by': obj.created_by, 'organization': obj.created_by.organization}) 
                    for row in data]
        [row.update({f'{field}_id': choices.get(name=row[field]).get('id') 
                    for field, choices in fields.items()}) for row in data]
        
        [row.pop(field) for field in fields.keys() for row in data]
        data = [model(**row) for row in data]

        model.objects.bulk_create(data, ignore_conflicts=True)
        Notification.objects.create(**{
            '_from': obj.created_by,
            '_to': obj.created_by,
            'subject': _('Importation réussie'),
            'message': _('Les données ont été importées avec succès'),
            'redirect': reverse_lazy('core:list', kwargs={'app': obj.content_type.app_label, 'model': obj.content_type.model})
        })
    except Exception as e:
        Notification.objects.create(**{
            '_from': obj.created_by,
            '_to': obj.created_by,
            'subject': _('Importation échouée'),
            'message': str(e),
        })
        obj.status = ImporterStatus.ERROR
        obj.message = str(e)
        obj.save()
        return

    obj.status = ImporterStatus.SUCCESS
    obj.save()