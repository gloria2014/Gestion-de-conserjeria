from django import forms
from .models import Prueba
from apps.authentication.models import Empleados, Region, Comuna
from apps.home.models import (
 Estacionamiento, NumeroEstacionamiento, UbicacionEstacionamiento, 
 TipoEstacionamiento, EstadoEstacionamiento,ReservaEstacionamiento,
  Propiedad, Residentes)


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

    class Meta:
        model = Empleados  # Asegúrate de que este es el modelo correcto
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion',
                   'telefono', 'correo_electronico', 'sexo', 'fecha_ingreso','id_region','id_comuna']

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
        super().__init__(*args, **kwargs)
        if 'id_region' in self.data:
            try:
                region_id = int(self.data.get('id_region'))
                self.fields['id_comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['id_comuna'].queryset = self.instance.id_region.comuna_set.order_by('nombre')


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
                "class": "form-control d-none",
                "id": "id_residente",
                "autocomplete": "off",
                "onchange": "actualizarDatosResidente()"
          
            }
        ),
        required=False,
        empty_label="Seleccione"
    )


    class Meta:
        model = ReservaEstacionamiento
        fields = [
            'numero_propiedad',  # Agregar el campo de búsqueda
            'propiedad',
            'residente',  # Agregar el campo de selección de residente
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
            'fecha_llegada_visita',
            'fecha_registro_visita'
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
            'fecha_registro_visita': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservaEstacionamientoForm, self).__init__(*args, **kwargs)
        if 'numero_propiedad' in self.data:
            try:
                numero_propiedad = self.data.get('numero_propiedad')
                propiedad = Propiedad.objects.get(numero_propiedad=numero_propiedad)
                self.fields['residente'].queryset = Residentes.objects.filter(propiedad=propiedad)
            except (ValueError, TypeError, Propiedad.DoesNotExist):
                self.fields['residente'].queryset = Residentes.objects.none()
        elif self.instance.pk:
            self.fields['residente'].queryset = self.instance.propiedad.residentes_set.all()




    numero_propiedad = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Propiedad'}))
    residente = forms.ModelChoiceField(
        queryset=Residentes.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_residente",
                "autocomplete": "off"
            }
        ),
        required=True,
        empty_label="Seleccione"
    )
    class Meta:
        model = ReservaEstacionamiento
        fields = [
            'numero_propiedad',  # Agregar el campo de búsqueda
            'propiedad',
            'residente',  # Agregar el campo de selección de residente
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