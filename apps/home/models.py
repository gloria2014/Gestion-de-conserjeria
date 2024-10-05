
from django.db import models

class Prueba(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, verbose_name='Titulo')
    descripcion = models.CharField(max_length=100, verbose_name='Descripcion')