# Generated by Django 5.1.1 on 2024-10-05 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_id_rol_empleado_id_rol_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='id_rol_id',
            new_name='id_rol',
        ),
    ]
