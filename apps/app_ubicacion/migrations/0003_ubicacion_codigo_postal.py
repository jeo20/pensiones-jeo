# Generated by Django 4.1.5 on 2023-06-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ubicacion', '0002_alter_ubicacion_localidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ubicacion',
            name='codigo_postal',
            field=models.CharField(blank=True, default='9400', max_length=8, verbose_name='Código Postal'),
        ),
    ]