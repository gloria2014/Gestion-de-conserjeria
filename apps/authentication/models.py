
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .validators import validate_rut

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


   
class User(AbstractUser):
    SUPERADMIN = 'superadmin'
    ADMIN_CONDOMINIO = 'admin_condominio'
    CONSERJE = 'conserje'

    ROLE_CHOICES = [
        (SUPERADMIN, 'Super Administrador'),
        (ADMIN_CONDOMINIO, 'Administrador del Condominio'),
        (CONSERJE, 'Conserje'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=CONSERJE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()
    
    def is_superadmin(self):
        return self.rol and self.rol.nombre == 'superadmin'

    def is_admin_condominio(self):
        return self.rol and self.rol.nombre == 'admin_condominio'

    def is_conserje(self):
        return self.rol and self.rol.nombre == 'conserje'   
    

    
class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Empleados(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)  
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    telefono = models.IntegerField()
    correo_electronico = models.CharField(max_length=50)
    sexo = models.CharField(max_length=50)
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_retiro = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE) 
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def save(self, *args, **kwargs):
        if not self.id_rol:
            self.id_rol_id = 1  # Establecer el valor predeterminado para id_rol
        super().save(*args, **kwargs)

