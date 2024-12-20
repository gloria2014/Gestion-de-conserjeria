# Generated by Django 4.2.3 on 2024-11-10 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condominio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=10)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.region')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoEstacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='NumeroEstacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_propiedad', models.IntegerField(unique=True)),
                ('piso', models.IntegerField()),
                ('estado', models.CharField(max_length=10)),
                ('estacionamiento', models.CharField(choices=[('SI', 'Sí'), ('NO', 'No')], default='NO', max_length=2)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('condominio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.condominio')),
            ],
        ),
        migrations.CreateModel(
            name='Prueba',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50, verbose_name='Titulo')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='TipoCondominio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoEstacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UbicacionEstacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Residentes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=12)),
                ('nombres', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('correo_electronico', models.CharField(max_length=50)),
                ('propietario', models.CharField(choices=[('SI', 'Sí'), ('NO', 'No')], max_length=2)),
                ('estado', models.CharField(max_length=10)),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.propiedad')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaEstacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estacionamiento', models.IntegerField(blank=True, null=True)),
                ('rut_visita', models.CharField(max_length=12)),
                ('nombre_visita', models.CharField(max_length=50)),
                ('apellido_paterno_visita', models.CharField(max_length=50)),
                ('apellido_materno_visita', models.CharField(max_length=50)),
                ('telefono_visita', models.CharField(max_length=10)),
                ('relacion_residente', models.CharField(max_length=50)),
                ('patente_vehiculo', models.CharField(blank=True, max_length=8, null=True)),
                ('descripcion_vehiculo', models.CharField(blank=True, max_length=100, null=True)),
                ('tiempo_permanencia', models.TimeField(blank=True, null=True)),
                ('fecha_registro_visita', models.DateTimeField(auto_now_add=True)),
                ('fecha_llegada_visita', models.DateTimeField(blank=True, null=True)),
                ('fecha_llegada_visita_confirmada', models.DateTimeField(blank=True, null=True)),
                ('fecha_modifica_reserva', models.DateTimeField(blank=True, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.empleados')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.propiedad')),
            ],
        ),
        migrations.CreateModel(
            name='Observaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_registro_observacion', models.DateTimeField(auto_now_add=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.empleados')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.propiedad')),
            ],
        ),
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('estado_estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.estadoestacionamiento')),
                ('numero_estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.numeroestacionamiento')),
                ('tipo_estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tipoestacionamiento')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ubicacionestacionamiento')),
            ],
        ),
        migrations.AddField(
            model_name='condominio',
            name='tipo_condominio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tipocondominio'),
        ),
    ]
