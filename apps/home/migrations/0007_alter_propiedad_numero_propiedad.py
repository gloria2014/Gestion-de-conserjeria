# Generated by Django 4.2.3 on 2024-10-19 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_condominio_comuna_alter_condominio_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedad',
            name='numero_propiedad',
            field=models.CharField(max_length=5),
        ),
    ]
