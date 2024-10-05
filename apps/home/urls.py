

from django.urls import path, re_path
from apps.home import views
from .views import load_comunas, load_regiones

urlpatterns = [

    # The home page
    path('', views.index, name='home'), # ESTA LINEA ES LA ORIGINAL 
    #path('', views.inicio, name='inicio'), # esta linea seria el inicio de la pagina del ejemplo de youtube
    
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
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
