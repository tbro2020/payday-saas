from django.utils.translation import gettext as _
from crispy_forms.layout import Layout

class Fielder:
    def get_form_fields(self, model):
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        if fields == '__all__':
            return fields

        if not self.is_approver():
            approver_fields = [field.name for field in model._meta.fields if getattr(field, 'approver', False)]
            fields = [field for field in fields if field not in approver_fields]
        return fields

    def get_inline_form_fields(self, model):
        if self.is_full_approved():
            return '__all__'

        fields = [field.name for field in model._meta.fields if getattr(field, 'inline', False) and not getattr(field, 'approver', False)]
        if self.is_approver():
            approver_fields = [field.name for field in model._meta.fields if getattr(field, 'inline', False) and getattr(field, 'approver', False)]
            fields.extend(approver_fields)
        return fields