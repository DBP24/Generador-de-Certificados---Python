from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import LoginForm
from apps.certificate.forms import CargarDocumentoForm
from apps.certificate.utils import cargar_hoja
from django.urls import reverse_lazy





class UserLoginView(LoginView):
  template_name = 'account/login.html'
  form_class = LoginForm

  def dispatch(self, request, *args, **kwargs): 
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('accounts:dashboard'))
        return super().dispatch(request, *args, **kwargs) 

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')



@login_required
def dashboard(request):
    if request.user.groups.filter(name="Administrador").exists():
        hojas =  cargar_hoja()
        opciones_archivo = [(hoja['properties']['title'], hoja['properties']['title']) for hoja in hojas]
        form = CargarDocumentoForm(opciones_archivo=opciones_archivo)
        context = {
            'form' : form
        }
        return render(request,'account/dashboard.html', context)
    else:
        # return render(request,'accounts/clients.html',{'section': 'Cliente'})
        logout(request)
        msg = "Usted no cuenta con permisos para acceder"
        return render(request,'account/login.html',{'msg': msg})
    
