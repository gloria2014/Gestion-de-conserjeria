# Generated by Django 4.2.3 on 2024-10-19 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('home', '0005_observaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominio',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.comuna'),
        ),
        migrations.AlterField(
            model_name='condominio',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.region'),
        ),
    ]
