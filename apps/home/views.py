
from django.shortcuts import render, redirect, get_object_or_404
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
from apps.authentication.models import Region, Comuna, Empleados, User
from apps.home.models import (
    Estacionamiento, TipoEstacionamiento, 
    UbicacionEstacionamiento, ReservaEstacionamiento, EstadoEstacionamiento,
    NumeroEstacionamiento, Propiedad, Residentes)

from .forms import( PruebaForm, EmpleadoForm, EstacionamientoForm,
 ReservaEstacionamientoForm)

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


@login_required(login_url="/login/")
def crear_conserje_view(request):
    #formulario = EmpleadoForm(request.POST or None)
    print("Rol del usuario actual   :::::", request.user.role)
    formulario = EmpleadoForm(request.POST or None, user=request.user)
   
    msg = None
    success = False

    if request.method == "POST":
        print("viene del post ::::: " ,request.POST)
        

        if formulario.is_valid():
            print("formulario valido ::::: " ,formulario)
            # Tomar los campos del formulario de empleado
            rut = formulario.cleaned_data.get("rut")        
            nombres = formulario.cleaned_data.get("nombres")
            apellido_paterno = formulario.cleaned_data.get("apellido_paterno")
            apellido_materno = formulario.cleaned_data.get("apellido_materno")
            email = formulario.cleaned_data.get("correo_electronico")
            username = email.split('@')[0]  # Usar parte del correo como nombre de usuario
            #raw_password = User.objects.make_random_password()  # Generar una contraseña aleatoria
            raw_password = formulario.cleaned_data.get("clave_temporal")  
           
            rol = formulario.cleaned_data.get("id_rol")

            # Validar que el rut no se repita en la tabla de empleados
            if Empleados.objects.filter(rut=rut).exists():
                msg = 'Empleado ya existe'
                return render(request, "home/registrar-conserje.html", {"formulario": formulario, "msg": msg, "success": success})

             # Validar que el nombre de usuario no se repita en la tabla de usuarios
            if User.objects.filter(username=username).exists():
                msg = 'Nombre de usuario ya existe'
                return render(request, "home/registrar-conserje.html", {"formulario": formulario, "msg": msg, "success": success})


            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=nombres,
                last_name=f"{apellido_paterno} {apellido_materno}"
            )
            user.set_password(raw_password)  # Encriptar la clave temporal
            user.rol = rol  # Asignar el id del rol al usuario
            user.role = rol.nombre  # Asignar el nombre del rol al usuario
            user.save()
            
            print("usuario creado ::::: " ,user)
            # Crear el empleado asociado al usuario
            empleado = formulario.save(commit=False)
            empleado.usuario = user
            empleado.save()  # Guardar el empleado primero para obtener un ID

            # Guardar las relaciones de muchos a muchos
            formulario.save_m2m()

            msg = 'Usuario creado con exito'
            success = True

            return redirect('ver_conserjes')
        else:
            print("Errores del formulario:", formulario.errors)
            msg = 'Form is not valid'

    return render(request, "home/registrar-conserje.html",{"formulario": formulario, "msg": msg, "success": success})

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

# -------------- SECCIÓN RESERVAS ----------------------------

@login_required(login_url="/login/")
def buscar_residentes(request):
    numero_propiedad = request.GET.get('numero_propiedad')
    if numero_propiedad:
        try:
            propiedad = Propiedad.objects.get(numero_propiedad=numero_propiedad)
            residentes = Residentes.objects.filter(propiedad=propiedad)
            residentes_list = [{'id': residente.id, 'nombre': f'{residente.nombres} {residente.apellido_paterno} {residente.apellido_materno}'} for residente in residentes]
            return JsonResponse({'residentes': residentes_list})
        except Propiedad.DoesNotExist:
            return JsonResponse({'error': 'Propiedad no encontrada'}, status=404)
    return JsonResponse({'error': 'Número de propiedad no proporcionado'}, status=400)

@login_required(login_url="/login/")
def obtener_datos_residente(request):   
    residente_id = request.GET.get('residente_id')
    if residente_id:
        try:
            residente = Residentes.objects.get(id=residente_id)
            datos_residente = {
                'nombre_completo': f'{residente.nombres} {residente.apellido_paterno} {residente.apellido_materno}',
                'telefono': residente.telefono
            }
            return JsonResponse(datos_residente)
        except Residentes.DoesNotExist:
            return JsonResponse({'error': 'Residente no encontrado'}, status=404)
    return JsonResponse({'error': 'ID de residente no proporcionado'}, status=400)

@login_required(login_url="/login/")
def obtener_datos_propiedad(request):    
    numero_propiedad = request.GET.get('numero_propiedad')
    if numero_propiedad:
        try:
            propiedad = Propiedad.objects.get(numero_propiedad=numero_propiedad)
            print("Propiedad ::::::::::::::::::::::.....: ", propiedad)
            datos_propiedad = {
                'id': propiedad.id,
                'numero_propiedad': propiedad.numero_propiedad,
                'piso': propiedad.piso,
                'estado': propiedad.estado
            }
            return JsonResponse(datos_propiedad)
        except Propiedad.DoesNotExist:
            return JsonResponse({'error': 'Propiedad no encontrada'}, status=404)
    return JsonResponse({'error': 'Número de propiedad no proporcionado'}, status=400)


@login_required(login_url="/login/")
def ver_reservas_view(request):
    query = Q()
    if 'rut_visita' in request.GET and request.GET['rut_visita']:
        query &= Q(rut_visita=request.GET['rut_visita'])

    if 'patente_vehiculo' in request.GET and request.GET['patente_vehiculo']:
        query &= Q(patente_vehiculo=request.GET['patente_vehiculo'])

    reservas = ReservaEstacionamiento.objects.filter(query)

    # Obtener los datos de las reservas y el número de estacionamiento si existe
    reservas_list = []
    for reserva in reservas:
        numero_estacionamiento = None
        if reserva.estacionamiento:
            try:
                numero_estacionamiento = NumeroEstacionamiento.objects.get(id=reserva.estacionamiento).numero
            except NumeroEstacionamiento.DoesNotExist:
                numero_estacionamiento = None

        reservas_list.append({
            'rut_visita': reserva.rut_visita,
            'nombre_completo': f"{reserva.nombre_visita} {reserva.apellido_paterno_visita} {reserva.apellido_materno_visita}",
            'relacion_residente': reserva.relacion_residente,
            'patente_vehiculo': reserva.patente_vehiculo,
            'descripcion_vehiculo': reserva.descripcion_vehiculo,
            'numero_estacionamiento': numero_estacionamiento,
            'fecha_registro_visita': reserva.fecha_registro_visita,
        })

    return render(request, 'home/ver-reservas.html', {'reservasObj': reservas_list})

@login_required(login_url="/login/")
def crear_reserva_view(request):
    msg = None
    # Obtenemos el formulario con los datos POST si están presentes
    empleado_id = request.session.get('empleado_id')
    initial_data = {'empleado_id': empleado_id}

    formulario = ReservaEstacionamientoForm(request.POST or None)
    print(" 1 request post::::::::::::::: ", request.POST)
    numero_propiedad = request.POST.get('propiedad', '').strip() or request.GET.get('numero_propiedad', '').strip()
    

    if numero_propiedad is not None:
        try:
            if isinstance(numero_propiedad, dict):
                numero_propiedad = numero_propiedad.get('id')
                numero_propiedad = int(numero_propiedad)
                print("numero_propiedad int ::::::::::::::: ", numero_propiedad)
        except ValueError:
            print("Error: numero_propiedad no es un número válido.")
            numero_propiedad = None
            msg = 'numero_propiedad no es un número válido'
    else:
        print("Error: numero_propiedad es None.")
        numero_propiedad = None


    print("numero_propiedad ::::::::::::::: ", numero_propiedad)
    residentes = None  # Inicializar la variable residentes
   
    if numero_propiedad:
        propiedad = Propiedad.objects.get(id=numero_propiedad)       
        datos_propiedad = {
                'id': propiedad.id,
                'numero_propiedad': propiedad.numero_propiedad,
                'piso': propiedad.piso,
                'estado': propiedad.estado
        }
        print("Propiedad resultado ::::::::::::::::::::::.....: ", datos_propiedad)

        # Iterar sobre las claves y valores del diccionario
        for key, value in datos_propiedad.items():
            print(f"{key}: {value}")

        residentes = Residentes.objects.filter(propiedad=datos_propiedad['id'])
        
        # Iterar sobre los objetos del QuerySet de Residentes
        for residente in residentes:
            print(f"Residente ID: {residente.id}, Nombre: {residente.nombres}, Propiedad ID: {residente.propiedad.id}")
        print("residentes despues del for ::::::::::::::::::::::.....: ", residentes)
        # Asigna el queryset de residentes a los campos del formulario
        formulario.fields['residente'].queryset = residentes



        if request.method == 'GET':
            print(" 2 rquest get ::::::::::::::: ", request.GET)
            # Configura los valores iniciales para el formulario
            formulario = ReservaEstacionamientoForm(initial={
                'propiedad': propiedad.id,
                'nombre_visita': residentes[0].nombres if residentes else '',
                'apellido_paterno_visita': residentes[0].apellido_paterno if residentes else '',
                'apellido_materno_visita': residentes[0].apellido_materno if residentes else '',
                'telefono_visita': residentes[0].telefono if residentes else '',
            })
        elif request.method == 'POST':
            print(" 3 rquest post ::::::::::::::: ", request.POST)
            print("Valor de 'residente' en request.POST:", request.POST.get('residente'))
            # Valida y guarda el formulario si es válido
            if formulario.is_valid():
                reserva = formulario.save(commit=False)

                # Asigna el ID del empleado logueado
                reserva.empleado_id = empleado_id
                
                reserva.save()  # Guarda la reserva
                return redirect('ver_reservas')
            else:
                messages.error(request, "Errores en el formulario. Por favor corrígelos.")
                print("Errores del formulario:", formulario.errors)
                msg = formulario.errors
        
        return render(request, 'home/registrar-reserva.html', {'formulario': formulario, 'residentes': residentes})

    return render(request, 'home/registrar-reserva.html', {'formulario': formulario, 'residentes': residentes, 'msg': msg})




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
    
    