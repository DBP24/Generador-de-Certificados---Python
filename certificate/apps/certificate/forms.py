from django import forms
from django.core.exceptions import ValidationError


class CargarDocumentoForm(forms.Form):
    name_hoja = forms.ChoiceField(
        label=None,
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, opciones_archivo=None, **kwargs):
        super().__init__(*args, **kwargs)
        if opciones_archivo:
            self.fields['name_hoja'].choices = opciones_archivo
    
    
    
