from django import forms
from django.core.exceptions import ValidationError


class CargarDocumentoForm(forms.Form):
    archivo_ruta = forms.CharField(
        label=None,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa en nombre de la hoja o identificador'})
    )
    
    
