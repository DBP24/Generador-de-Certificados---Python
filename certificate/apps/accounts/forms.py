import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import gettext_lazy as _



class LoginForm(AuthenticationForm):
  username = UsernameField(
      widget=forms.TextInput(attrs={"class": "input100", "placeholder": "Usuario"}),
      error_messages={
            'required': _("El campo de usuario es obligatorio."),
        }
      )
  password = forms.CharField(
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Contraseña"}),
      error_messages={
        'required': 'El campo de contraseña es obligatorio',
        'min_length': 'La contraseña debe tener al menos %(limit_value)d caracteres'
    },
    min_length=4
  )

  error_messages = {
        'invalid_login': "Las credenciales que has proporcionado no son válidas. Por favor, inténtalo de nuevo.",
        'inactive': _("Esta cuenta está inactiva."),
    }
  
  def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError(_("El nombre de usuario solo puede contener letras y números."))
        return username
  
