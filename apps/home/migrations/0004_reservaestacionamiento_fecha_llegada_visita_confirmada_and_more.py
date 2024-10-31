# Generated by Django 4.2.3 on 2024-10-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_residentes_rut'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservaestacionamiento',
            name='fecha_llegada_visita_confirmada',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservaestacionamiento',
            name='fecha_llegada_visita',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservaestacionamiento',
            name='fecha_modifica_reserva',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
