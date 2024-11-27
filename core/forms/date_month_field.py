from django_filters.widgets import SuffixedMultiWidget
from django import forms

class DateRangeWidget(SuffixedMultiWidget):
    template_name = "django_filters/widgets/multiwidget.html"
    suffixes = ["after", "before"]

    def __init__(self, attrs=None):
        widgets = (forms.DateInput(attrs={'type': 'date'}), forms.DateInput(attrs={'type': 'date'}))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]