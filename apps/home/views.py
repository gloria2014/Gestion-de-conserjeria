
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse

from django.template.loader import render_to_string
from weasyprint import HTML

from .models import Prueba
from apps.authentication.models import Region, Comuna, Empleados

from .forms import PruebaForm, EmpleadoForm

import logging

logger = logging.getLogger(__name__)

# Esta funcion es el ejemplo de la pagina de youtube. NO se usan 
@login_required(login_url="/login/")
def inicio(request):
    return HttpResponse("<h1>bienvenido a home </h1>")

#------ fin ejemplo yotube ---


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# ----------------- REGION Y COMUNAS ---------------------------
# AJAX
def load_regiones(request):
    logger.debug("Loading regions")
    regiones = Region.objects.all().values('id', 'nombre')
    logger.debug(f"Regiones: {list(regiones)}")
    return JsonResponse(list(regiones), safe=False)

def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

# ----------------- RUTAS PARA IR A LAS PAGINAS  CONSERJE GESTION ---------------------------

@login_required(login_url="/login/")
def ver_conserjes_view(request):
    empleados = Empleados.objects.all()
    return render(request, 'home/ver-empleados.html', {'empleadosObj':empleados})

@login_required(login_url="/login/")
def crear_conserje_view(request):
    formulario = EmpleadoForm(request.POST or None)

    if request.method == 'POST':
        print(request.POST)
    
    if formulario.is_valid():
        formulario.save()
        return redirect('ver_conserjes') # aca estoy llamado a la url del home : 'ver_observaciones'
    else:
        print("Errores del formulario:", formulario.errors)
        messages.error(request, "Hay errores en el formulario. Por favor, corrígelos.")


    return render(request, 'home/registrar-conserje.html', {'formulario':formulario})

@login_required(login_url="/login/")
def editar_conserje_view(request, id):   
    empleado = Empleados.objects.get(id=id)
    
    # Imprime todos los campos del objeto prueba en la consola
    for field in empleado._meta.fields:
        field_name = field.name
        field_value = getattr(empleado, field_name)
        print(f"{field_name}: {field_value}")

    formulario = EmpleadoForm(request.POST or None, instance=empleado)

    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ver_conserjes')

    return render(request, 'home/editar-conserje.html', {'formulario':formulario})


@login_required(login_url="/login/")
def eliminar_conserje_view(request, id):
    prueba = Empleados.objects.get(id=id)
    prueba.delete()
    return redirect('ver_conserjes') 
    
@login_required(login_url="/login/")
def exportar_conserjes_pdf(request):
    conserjes = Empleados.objects.all()
    html_string = render_to_string('home/empleados-pdf.html', {'empleados': conserjes})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=conserjes.pdf'
    html.write_pdf(response)
    return response


# ----------------- RUTAS PARA IR A LAS PAGINAS  DE OBSERVACIONES ---------------------------

@login_required(login_url="/login/")
def ver_observaciones_view(request):
    pruebas = Prueba.objects.all()
    print(pruebas)
    return render(request,'home/ver-observaciones.html', {'pruebasObj':pruebas})
    

@login_required(login_url="/login/")
def crear_observacion_view(request):
    formulario = PruebaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('ver_observaciones') # aca estoy llamado a la url del home : 'ver_observaciones'

    return render(request, 'home/registrar-observacion.html', {'formulario':formulario})


@login_required(login_url="/login/")
def editar_observacion_view(request, id):
    prueba = Prueba.objects.get(id=id)
    
    # Imprime todos los campos del objeto prueba en la consola
    for field in Prueba._meta.fields:
        field_name = field.name
        field_value = getattr(prueba, field_name)
        print(f"{field_name}: {field_value}")

    formulario = PruebaForm(request.POST or None, instance=prueba)

    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ver_observaciones')

    return render(request, 'home/editar-observacion.html', {'formulario':formulario})





@login_required(login_url="/login/")
def eliminar_observacion_view(request, id):
    obj = Prueba.objects.get(id=id)
    obj.delete()
    return redirect('ver_observaciones') 
    
    