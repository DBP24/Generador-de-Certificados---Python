from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils import leerGoogleSheets
from django.http import HttpResponse
from .forms import CargarDocumentoForm
from django.contrib import messages

@login_required
def brind_dat(request):
    if request.method == 'POST':
        form = CargarDocumentoForm(request.POST)
        if form.is_valid():
            name_hoja    = form.cleaned_data['archivo_ruta']
            data = leerGoogleSheets(name_hoja)
            try:
                form = CargarDocumentoForm()
                context = {
                    'form': form,
                    'encabezados' : data[0],
                    'contenido' : data[1:]
                }
                return render(request, 'account/dashboard.html', context)
            except Exception as e:
                messages.error(request, f"Hubo un error alsolicitar datos: {str(e)}")
        else:
            # Mensajes de error del formulario
            for error in form.non_field_errors():
                messages.error(request, error)

    return redirect("accounts:dashboard")
 