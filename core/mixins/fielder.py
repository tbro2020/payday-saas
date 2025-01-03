from django.forms import inlineformset_factory, modelform_factory
from django.utils.translation import gettext as _

from crispy_forms.layout import Layout
from django.apps import apps

class FielderMixin:

    def inline_model_form(self, model):
        form_class = modelform_factory(model, fields=self.get_inline_form_fields(model))
        form_instance = self.filter_form(form_class())
        del form_class

        return modelform_factory(
            model, 
            fields=self.get_inline_form_fields(model),
            widgets={field: form_instance.fields[field].widget for field in form_instance.fields}
        )


    def formsets(self, can_delete=True, extra=1):
        model = self.get_model()
        inlines = getattr(model, 'inlines', tuple())
        formsets = [apps.get_model(*inline.split('.')) for inline in inlines]
        formsets = [inlineformset_factory(
            model, 
            inline,
            self.inline_model_form(inline),
            fields=self.get_inline_form_fields(inline), 
            can_delete=can_delete, 
            extra=extra
        ) for inline in formsets]

        return formsets

    def filter_form(self, form):
        if self.request.user.is_superuser: 
            return form

        level, add = 0, True
        form = form() if isinstance(form, type) else form
        permissions = self.request.user.get_user_permissions(**{
            'content_type__app_label': form.Meta.model._meta.app_label,
            'content_type__model': form.Meta.model._meta.model_name
        }).values_list('level', 'add').distinct() or [(level, add)]

        level, add = zip(*((perm[0], perm[1]) for perm in permissions))
        level, add = min(level), any(add)

        for field in form.fields:
            _field = form.Meta.model._meta.get_field(field)
            _level = getattr(_field, 'level', 0)
            if all([add, _level <= level]): continue
            form.fields[field].widget.attrs['readonly'] = True
            form.fields[field].widget.attrs['class'] = 'bg-dark'

        return form

    def get_form_fields(self, model=None):
        model = model or self.get_model()
        fields = getattr(model, 'layout', Layout())
        return [field.name for field in fields.get_field_names()]

    def get_inline_form_fields(self, model=None):
        model = model or self.get_model()
        return [field.name for field in model._meta.fields if getattr(field, 'inline', False)]