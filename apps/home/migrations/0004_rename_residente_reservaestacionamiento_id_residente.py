# Generated by Django 4.2.3 on 2024-11-17 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_reservaestacionamiento_residente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservaestacionamiento',
            old_name='residente',
            new_name='id_residente',
        ),
    ]
