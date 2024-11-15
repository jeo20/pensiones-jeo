# Generated by Django 4.1.5 on 2023-01-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_numerico', models.PositiveIntegerField(unique=True)),
                ('descripcion_corta', models.CharField(max_length=4)),
                ('descripcion', models.CharField(max_length=25)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
