# Generated by Django 4.1.5 on 2023-07-20 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ubicacion', '0003_ubicacion_codigo_postal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ubicacion',
            options={'ordering': ['localidad', 'nombre', 'codigo_postal']},
        ),
        migrations.AddIndex(
            model_name='ubicacion',
            index=models.Index(fields=['localidad'], name='app_ubicaci_localid_24b721_idx'),
        ),
        migrations.AddIndex(
            model_name='ubicacion',
            index=models.Index(fields=['nombre'], name='app_ubicaci_nombre_f2a4db_idx'),
        ),
        migrations.AddConstraint(
            model_name='ubicacion',
            constraint=models.UniqueConstraint(fields=('localidad',), name='localidad'),
        ),
    ]