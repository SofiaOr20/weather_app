from django.core.validators import FileExtensionValidator
from django import forms


class DocumentForm(forms.Form):
    city = forms.CharField(label='Enter city name', max_length=80)
    file = forms.FileField(label='Select a file', validators=[FileExtensionValidator(allowed_extensions=["csv"])])


class RecordUpdateForm(forms.Form):
    temperature_avg = forms.FloatField(label='Average temperature', min_value=-60, max_value=50)
    temperature_min = forms.FloatField(label='Minimal temperature', min_value=-60, max_value=50)
    temperature_max = forms.FloatField(label='Maximum temperature', min_value=-60, max_value=50)
    date = forms.DateField(widget=forms.HiddenInput())
