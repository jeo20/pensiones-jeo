# Generated by Django 4.1.5 on 2023-04-10 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_beneficiarios', '0005_alter_beneficiario_options_and_more'),
        ('app_id_liquidacion', '0004_alter_idliquidacion_fecha_pago'),
        ('app_codigos', '0005_codigo_modificado_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoMensual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateField(auto_now=True)),
                ('modificado_usuario', models.CharField(default='ADMIN', max_length=30)),
                ('beneficiario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_beneficiarios.beneficiario')),
                ('codigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_codigos.codigo')),
                ('id_liquidacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_id_liquidacion.idliquidacion')),
            ],
        ),
    ]
