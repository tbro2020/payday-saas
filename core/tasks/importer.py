from django.utils.translation import gettext as _
from celery import shared_task
from django.apps import apps
import pandas as pd

from core.message import message_user
from core.models import ImporterStatus

from django.template import loader

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

        message_user(obj.created_by, _('L\'importation a échoué en raison d\'un problème d\'autorisation'))
        obj.created_by.email_user(**{
            'subject': _(f'PayDay | L\'importation du/de {obj.content_type.model} a échoué'),
            'message': loader.render_to_string('email/importation_failed.txt')
        })

    # Update status
    obj.status = ImporterStatus.PROCESSING
    obj.save()

    # Get model
    model = obj.content_type.model_class()
    fields = {field.verbose_name:field for field in model._meta.fields}
    
    # Read excel file
    df = pd.read_excel(obj.document)
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
    except Exception as e:
        message_user(obj.created_by, _(f'L\'importation a échoué en de : {str(e)}'))
        obj.status = ImporterStatus.ERROR
        obj.message = str(e)
        obj.save()
        return

    message_user(obj.created_by, _(f'L\'importation de {model._meta.verbose_name} est effectuée'))
    obj.status = ImporterStatus.SUCCESS
    obj.save()

    obj.created_by.email_user(**{
        'subject': _(f'PayDay | L\'importation du/de {obj.content_type.model} réussie'),
        'message': loader.render_to_string('email/importation_success.txt')
    })