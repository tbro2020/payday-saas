from django.apps import apps

class Documentor:
    def documents(self):
        template_model = apps.get_model('core', 'template')
        app, model = self.kwargs['app'], self.kwargs['model']
        return template_model.objects.filter(
            content_type__app_label=app,
            content_type__model=model
        ).values('id', 'name')