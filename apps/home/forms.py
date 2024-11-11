from django import forms
from .models import Prueba
from apps.authentication.models import(
    Empleados, Region, Comuna, Rol, User)

from apps.home.models import (
 Estacionamiento, NumeroEstacionamiento, UbicacionEstacionamiento, 
 TipoEstacionamiento, EstadoEstacionamiento,ReservaEstacionamiento,
  Propiedad, Residentes)

from django.contrib.auth.password_validation import validate_password



class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['id', 'titulo', 'descripcion']  # Especifica los campos que quieres incluir

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    titulo = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(PruebaForm, self).__init__(*args, **kwargs)
        self.fields['id'].label = ''  # Oculta la etiqueta del campo id

    def __str__(self):
        return self.titulo
    

class DateInput(forms.DateInput):
    input_type = 'date'

class EmpleadoForm(forms.ModelForm):
    id_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_region",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
    id_comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_comuna",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )

    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_rol",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
   

    clave_temporal = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Clave Temporal",
                "autocomplete": "off"
            }
        ),
        required=True
    )

    class Meta:
        model = Empleados  # Asegúrate de que este es el modelo correcto
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion',
                   'telefono', 'correo_electronico', 'sexo', 'fecha_ingreso','id_region',
                   'id_comuna', 'id_rol','clave_temporal']

        widgets = {
            'fecha_ingreso': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_fecha_ingreso', 'autocomplete': 'off'}),
        #   'fecha_retiro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_fecha_retiro'}),
          
            }
    
    
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '111111111-1', 'autocomplete': 'off'}))
    apellido_paterno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    sexo = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'autocomplete': 'off'}),
        choices=[('M', 'Masculino'), ('F', 'Femenino')]
    )
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo_electronico = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))

  
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limitamos el queryset de id_rol según el rol del usuario actual
            if user.role == 'admin_condominio':
                self.fields['id_rol'].queryset = Rol.objects.filter(nombre='conserje')
            elif user.role == 'super_admin':
                self.fields['id_rol'].queryset = Rol.objects.filter(nombre__in=['admin_condominio', 'conserje'])

             # Imprimir los roles disponibles en el queryset para verificar
            print("Roles disponibles en el formulario:", self.fields['id_rol'].queryset)


        roles = Rol.objects.all()
        print("roles disponibles:")
        for rol in roles:
            print(f"ID: {rol.id}, Nombre: {rol.nombre}")

        if 'id_region' in self.data:
            try:
                region_id = int(self.data.get('id_region'))
                self.fields['id_comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['id_comuna'].queryset = self.instance.id_region.comuna_set.order_by('nombre')

class EmpleadoEditForm(forms.ModelForm):
    id_region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_region",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
    id_comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_comuna",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )

    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_rol",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
   


    class Meta:
        model = Empleados  # Asegúrate de que este es el modelo correcto
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'fecha_ingreso',
                   'id_rol','direccion', 'telefono', 'correo_electronico', 'id_region',
                   'id_comuna']

        widgets = {
            'fecha_ingreso': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_fecha_ingreso', 'autocomplete': 'off'}),
        #   'fecha_retiro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_fecha_retiro'}),
          
            }
    
    
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '111111111-1', 'autocomplete': 'off'}))
    apellido_paterno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    sexo = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'autocomplete': 'off'}),
        choices=[('M', 'Masculino'), ('F', 'Femenino')]
    )
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo_electronico = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))

  
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limitamos el queryset de id_rol según el rol del usuario actual
            if user.role == 'admin_condominio':
                self.fields['id_rol'].queryset = Rol.objects.filter(nombre='conserje')
            elif user.role == 'super_admin':
                self.fields['id_rol'].queryset = Rol.objects.filter(nombre__in=['admin_condominio', 'conserje'])

             # Imprimir los roles disponibles en el queryset para verificar
            print("Roles disponibles en el formulario:", self.fields['id_rol'].queryset)


        roles = Rol.objects.all()
        print("roles disponibles:")
        for rol in roles:
            print(f"ID: {rol.id}, Nombre: {rol.nombre}")

        if 'id_region' in self.data:
            try:
                region_id = int(self.data.get('id_region'))
                self.fields['id_comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['id_comuna'].queryset = self.instance.id_region.comuna_set.order_by('nombre')

        # Deshabilitar campos específicos
        disabled_fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'fecha_ingreso', 'id_rol']
        for field in disabled_fields:
            self.fields[field].widget.attrs['disabled'] = True

class EstacionamientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EstacionamientoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si estamos editando, mostrar el número de estacionamiento actual
            self.fields['numero_estacionamiento'].queryset = NumeroEstacionamiento.objects.filter(pk=self.instance.numero_estacionamiento.pk)
            
        else:
            # Si estamos creando, mostrar solo los números de estacionamiento disponibles
            self.fields['numero_estacionamiento'].queryset = NumeroEstacionamiento.objects.filter(estado='1')

    numero_estacionamiento = forms.ModelChoiceField(
        queryset=NumeroEstacionamiento.objects.none(),  # Se establece en __init__
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_numero_estacionamiento",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )

    ubicacion = forms.ModelChoiceField(
        queryset=UbicacionEstacionamiento.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_ubicacion",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
    tipo_estacionamiento = forms.ModelChoiceField(
        queryset=TipoEstacionamiento.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_tipo_estacionamiento",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
    estado_estacionamiento = forms.ModelChoiceField(
        queryset=EstadoEstacionamiento.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_estado_estacionamiento",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )

    class Meta:
        model = Estacionamiento
        fields = ['numero_estacionamiento', 'ubicacion', 'tipo_estacionamiento', 'estado_estacionamiento']


class ReservaEstacionamientoForm(forms.ModelForm):
    numero_propiedad = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Propiedad'})
    )
    
    residente = forms.ModelChoiceField(
        queryset=Residentes.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "form-control d-none",  # Cambiar a d-none si quieres que sea invisible
                "id": "id_residente",
                "autocomplete": "off",
                "onchange": "actualizarDatosResidente()"  # Asume que tienes una función JavaScript
            }
        ),
        required=True,
        empty_label="Seleccione"
    )

    class Meta:
        model = ReservaEstacionamiento
        fields = [
            'numero_propiedad',  # Campo de búsqueda
            'propiedad',
            'residente',          # Campo de selección de residente
            'estacionamiento',
            'empleado',
            'rut_visita',
            'nombre_visita',
            'apellido_paterno_visita',
            'apellido_materno_visita',
            'telefono_visita',
            'relacion_residente',
            'patente_vehiculo',
            'descripcion_vehiculo',
            'tiempo_permanencia',
            'fecha_llegada_visita'
        ]
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-control'}),
            'estacionamiento': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'rut_visita': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_visita': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno_visita': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno_visita': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_visita': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion_residente': forms.TextInput(attrs={'class': 'form-control'}),
            'patente_vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'tiempo_permanencia': forms.TimeInput(attrs={'class': 'form-control'}),
            'fecha_llegada_visita': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si el campo 'numero_propiedad' está en los datos del formulario
        if 'numero_propiedad' in self.data:
            try:
                numero_propiedad = self.data.get('numero_propiedad')
                propiedad = Propiedad.objects.get(numero_propiedad=numero_propiedad)
                
                # Carga los residentes correspondientes a la propiedad
                self.fields['residente'].queryset = Residentes.objects.filter(propiedad=propiedad)
                
            except (ValueError, TypeError, Propiedad.DoesNotExist):
                self.fields['residente'].queryset = Residentes.objects.none()
        
        # Si el formulario se edita en modo instancia (al editar un objeto existente)
        elif self.instance.pk:
            self.fields['residente'].queryset = self.instance.propiedad.residentes_set.all()

    def clean_residente(self):
        # Obtén el valor de 'residente' del formulario
        residente = self.cleaned_data.get('residente')
        
        # Asegurarse de que 'residente' esté en el queryset actual
        if residente and residente not in self.fields['residente'].queryset:
            raise forms.ValidationError("Seleccione una opción válida para el residente.")
        
        return residente


class ProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Nueva Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Confirmar Nueva Contraseña",
        max_length=15
    )

    class Meta:
        model = User
        fields = ['new_password', 'confirm_password']
      

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        if new_password == "" or confirm_password == "":
            self.add_error('confirm_password', "Debe ingresar su nueva clave")
            

        if new_password:
            validate_password(new_password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user