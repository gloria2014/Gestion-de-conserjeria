# Generated by Django 5.1.1 on 2024-10-05 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_empleado_rut'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='id_rol',
            new_name='id_rol_id',
        ),
    ]
