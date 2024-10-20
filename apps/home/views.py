
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
from django.db.models import Q
from apps.authentication.models import Region, Comuna, Empleados
from apps.home.models import Estacionamiento, TipoEstacionamiento, UbicacionEstacionamiento, ReservaEstacionamiento, EstadoEstacionamiento, NumeroEstacionamiento

from .forms import PruebaForm, EmpleadoForm, EstacionamientoForm

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

# ----------------- REGION, COMUNAS, NUMERO-EST. ---------------------------
# LLAMDAS AJAX
def load_regiones(request):
    logger.debug("Loading regions")
    regiones = Region.objects.all().values('id', 'nombre')
    logger.debug(f"Regiones: {list(regiones)}")
    return JsonResponse(list(regiones), safe=False)

def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)


# ----------------- SECCIÓN  CONSERJE GESTION ---------------------------

@login_required(login_url="/login/")
def ver_conserjes_view_sinfiltro(request):
    empleados = Empleados.objects.all()
    return render(request, 'home/ver-empleados.html', {'empleadosObj':empleados})


@login_required(login_url="/login/")
def ver_conserjes_view(request):
    query = Q()
    if 'rut' in request.GET and request.GET['rut']:
        query &= Q(rut__icontains=request.GET['rut'])
    if 'nombres' in request.GET and request.GET['nombres']:
        query &= (
            Q(nombres__icontains=request.GET['nombres']) |
            Q(apellido_paterno__icontains=request.GET['nombres']) |
            Q(apellido_materno__icontains=request.GET['nombres'])
        )
    if 'correo_electronico' in request.GET and request.GET['correo_electronico']:
        query &= Q(correo_electronico__icontains=request.GET['correo_electronico'])

    empleados = Empleados.objects.filter(query)
    return render(request, 'home/ver-empleados.html', {'empleadosObj': empleados})


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


# ------------------------ SECCIÓN ESTACIONAMIENTOS MANTENEDOR  --------------------

# @login_required(login_url="/login/")
# def ver_estacionamientos_view(request):
#     query = Q()
#     if 'numero_estacionamiento' in request.GET and request.GET['numero_estacionamiento']:
#         query &= Q(rut__icontains=request.GET['numero_estacionamiento'])

#     if 'ubicacion' in request.GET and request.GET['ubicacion']:   
#         query &= Q(ubicacion=request.GET['ubicacion'])

#     if 'tipo_estacionamiento' in request.GET and request.GET['tipo_estacionamiento']:
#         query &= Q(tipo_estacionamiento=request.GET['tipo_estacionamiento'])

#     if 'estado_estacionamiento' in request.GET and request.GET['estado_estacionamiento']:
#         query &= Q(estado_estacionamiento=request.GET['estado_estacionamiento'])

#     estacionamientos = Estacionamiento.objects.filter(query)
#     return render(request, 'home/ver-estacionamientos.html', {'estacionamientosObj': estacionamientos})

@login_required(login_url="/login/")
def ver_estacionamientos_view(request):
    query = Q()
    if 'numero_estacionamiento' in request.GET and request.GET['numero_estacionamiento']:
        query &= Q(numero_estacionamiento=request.GET['numero_estacionamiento'])

    if 'ubicacion' in request.GET and request.GET['ubicacion']:   
        query &= Q(ubicacion=request.GET['ubicacion'])

    if 'tipo_estacionamiento' in request.GET and request.GET['tipo_estacionamiento']:
        query &= Q(tipo_estacionamiento=request.GET['tipo_estacionamiento'])

    if 'estado_estacionamiento' in request.GET and request.GET['estado_estacionamiento']:
        query &= Q(estado_estacionamiento=request.GET['estado_estacionamiento'])

    estacionamientos = Estacionamiento.objects.filter(query)
    
    # Obtener las opciones para los filtros
    numeros_estacionamiento = NumeroEstacionamiento.objects.all()
    ubicaciones = UbicacionEstacionamiento.objects.all()
    tipos_estacionamiento = TipoEstacionamiento.objects.all()
    estados_estacionamiento = EstadoEstacionamiento.objects.all()

    return render(request, 'home/ver-estacionamientos.html', {
        'estacionamientosObj': estacionamientos,
        'numeros_estacionamiento': numeros_estacionamiento,
        'ubicaciones': ubicaciones,
        'tipos_estacionamiento': tipos_estacionamiento,
        'estados_estacionamiento': estados_estacionamiento,
    })

@login_required(login_url="/login/")
def crear_estacionamiento_view(request):
    formulario = EstacionamientoForm(request.POST or None)

    if request.method == 'POST':
        print(request.POST)
    
        if formulario.is_valid():
            estacionamiento = formulario.save()
            # Actualizar el estado del NumeroEstacionamiento
            numero_estacionamiento = estacionamiento.numero_estacionamiento
            numero_estacionamiento.estado = '0'
            numero_estacionamiento.save()
            return redirect('ver_estacionamientos')
        else:
            messages.error(request, "Hay errores en el formulario. Por favor, corrígelos.")

            print("Errores del formulario:", formulario.errors)

    return render(request, 'home/registrar-estacionamiento.html',{'formulario':formulario})


@login_required(login_url="/login/")
def editar_estacionamiento_view(request, id):   
    estacionamiento = Estacionamiento.objects.get(id=id)
    
    # Imprime todos los campos del objeto prueba en la consola
    for field in estacionamiento._meta.fields:
        field_name = field.name
        field_value = getattr(estacionamiento, field_name)
        print(f"{field_name}: {field_value}")

    formulario = EstacionamientoForm(request.POST or None, instance=estacionamiento)

    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ver_estacionamientos')
    else:
        print("Errores del formulario:", formulario.errors)
        messages.error(request, "Hay errores en el formulario. Por favor, corrígelos.")
  
    return render(request, 'home/editar-estacionamiento.html', {
        'formulario': formulario,
        'numero_estacionamiento_hidden': formulario['numero_estacionamiento'].value()
    })



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
    
    