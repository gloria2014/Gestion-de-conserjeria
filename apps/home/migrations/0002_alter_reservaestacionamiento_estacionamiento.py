# Generated by Django 4.2.3 on 2024-11-02 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservaestacionamiento',
            name='estacionamiento',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]