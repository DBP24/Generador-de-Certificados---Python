from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils import leerGoogleSheets
from django.http import HttpResponse
from .forms import CargarDocumentoForm
from .utils import *
from django.contrib import messages

datos = None

@login_required
def brind_dat(request):
    hojas =  cargar_hoja()
    opciones_archivo = [(hoja['properties']['title'], hoja['properties']['title']) for hoja in hojas]
    if request.method == 'POST':
        form = CargarDocumentoForm(request.POST, request.FILES, opciones_archivo=opciones_archivo)
        if form.is_valid():
            name_hoja = form.cleaned_data['name_hoja']
            data = leerGoogleSheets(name_hoja)
            global datos
            datos =  data
            try:
                
                context = {
                    'form': form,
                    'encabezados' : data[0], 
                    'contenido' : data[1:],
                    'name_hoja' : name_hoja,
                    'identifier' : name_hoja[-1]
                }
                return render(request, 'account/dashboard.html', context)
            except Exception as e:
                messages.error(request, f"Hubo un error alsolicitar datos: {str(e)}")
        else:
            # Mensajes de error del formulario
            for error in form.non_field_errors():
                messages.error(request, error)

    return redirect("accounts:dashboard")
 

def recuper(response):
    global datos
    createCertificate(datos)
    return HttpResponse(f'se creo con exito los certificados')

from django.conf import settings
def listCertificate(request):
    documents_path = os.path.join(settings.MEDIA_ROOT, 'certificadosAlumnos')  # Directorio donde están los certificados
    try:
        files = os.listdir(documents_path)
    except FileNotFoundError:
        files = []

    context = {
        'files': files
    }
    return render(request, 'certificate/list_certificate.html', context)

from django.http import FileResponse, Http404

def download_certificate(request, filename):
    documents_path = os.path.join(settings.MEDIA_ROOT, 'certificadosAlumnos')
    file_path = os.path.join(documents_path, filename)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    # Serve the file
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    return response 


