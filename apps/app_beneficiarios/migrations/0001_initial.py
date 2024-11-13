# Generated by Django 4.1.5 on 2023-01-26 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_tipo_pensiones', '0001_initial'),
        ('app_ubicacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legajo', models.PositiveIntegerField()),
                ('apellido_y_nombre', models.CharField(max_length=40)),
                ('tipo_doc', models.CharField(choices=[('3', 'DNI'), ('0', 'OTRO')], max_length=1)),
                ('documento', models.PositiveIntegerField(unique=True)),
                ('direccion', models.CharField(default='SIN INFORMACION DISPONIBLE', max_length=40)),
                ('cobra_sac', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('tipo_pension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tipo_pensiones.tipopension')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_ubicacion.ubicacion')),
            ],
            options={
                'ordering': ['ubicacion', 'legajo'],
            },
        ),
    ]
