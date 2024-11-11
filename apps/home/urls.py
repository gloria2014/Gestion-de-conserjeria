

from django.urls import path, re_path
from apps.home import views
from .views import (load_comunas, load_regiones, buscar_residentes, 
obtener_datos_residente, obtener_datos_propiedad)

urlpatterns = [

    # The home page
    path('', views.index, name='home'), # ESTA LINEA ES LA ORIGINAL 
    #path('', views.inicio, name='inicio'), # esta linea seria el inicio de la pagina del ejemplo de youtube
    
    path('profile/', views.profile_view, name='profile'),
    path('inicio/', views.index, name='inicio'),

    path('ver-observaciones/', views.ver_observaciones_view, name='ver_observaciones'),
    path('crear-observacion/', views.crear_observacion_view, name='crear_observacion'),
    path('editar-observacion/', views.editar_observacion_view, name='editar_observacion'),
    path('eliminar-observacion/<int:id>', views.eliminar_observacion_view, name='eliminar_observacion'),
    path('editar-observacion/<int:id>', views.editar_observacion_view, name='editar_observacion'),

    path('ajax/load-comunas/', load_comunas, name='ajax_load_comunas'), # AJAX
    path('ajax/load-regiones/', load_regiones, name='ajax_load_regiones'),
   
    path('nuevo-conserje/', views.crear_conserje_view, name='crear_conserje'),
    path('conserjes/', views.ver_conserjes_view, name='ver_conserjes'),
    path('editar-conserje/', views.editar_conserje_view, name='editar_conserje'),
    path('editar-conserje/<int:id>', views.editar_conserje_view, name='editar_conserje'),
    path('eliminar-conserje/<int:id>', views.eliminar_conserje_view, name='eliminar_conserje'),
    path('empleados-pdf/', views.exportar_conserjes_pdf, name='exportar_empleados_pdf'),


    path('estacionamientos/', views.ver_estacionamientos_view, name='ver_estacionamientos'),
    path('nuevo-estacionamiento/', views.crear_estacionamiento_view, name='crear_estacionamiento'),
    path('editar-estacionamiento/<int:id>', views.editar_estacionamiento_view, name='editar_estacionamiento'), 


    path('reservas/', views.ver_reservas_view, name='ver_reservas'),
    path('nueva-reserva/', views.crear_reserva_view, name='crear_reserva'), 
    #path('nueva-reserva/', crear_reserva_view, name='crear_reserva'),

    path('buscar-residentes/', buscar_residentes, name='buscar_residentes'),  
    path('obtener-datos-residente/', obtener_datos_residente, name='obtener_datos_residente'),
    path('obtener-datos-propiedad/', obtener_datos_propiedad, name='obtener_datos_propiedad'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
