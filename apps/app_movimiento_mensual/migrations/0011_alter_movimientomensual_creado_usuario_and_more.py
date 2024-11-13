# Generated by Django 4.1.5 on 2023-08-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_movimiento_mensual', '0010_movimientomensual_tipo_carga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientomensual',
            name='creado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
        migrations.AlterField(
            model_name='movimientomensual',
            name='modificado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
        migrations.AlterField(
            model_name='movimientomensual',
            name='tipo_carga',
            field=models.CharField(choices=[('U', 'Carga Manual'), ('M', 'Carga Masiva desde Archivo'), ('A', 'Carga a través de API')], default='U', max_length=1),
        ),
    ]
