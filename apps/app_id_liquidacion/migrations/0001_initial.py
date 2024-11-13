# Generated by Django 4.1.5 on 2023-01-26 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdLiquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.PositiveIntegerField()),
                ('mes', models.CharField(choices=[('01ENE', 'ENERO'), ('02FEB', 'FEBRERO'), ('03MRZ', 'MARZO'), ('04ABR', 'ABRIL'), ('05MAY', 'MAYO'), ('06JUN', 'JUNIO'), ('07JUL', 'JULIO'), ('08AGO', 'AGOSTO'), ('09SEP', 'SEPTIEMBRE'), ('10OCT', 'OCTUBRE'), ('11NOV', 'NOVIEMBRE'), ('12DIC', 'DICIEMBRE'), ('13SC1', 'SAC PRIMERA CUOTA'), ('14SC2', 'SAC SEGUNDA CUOTA')], max_length=5)),
                ('descripcion', models.CharField(max_length=40)),
                ('cerrado', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
