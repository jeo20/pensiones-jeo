# Generated by Django 4.1.5 on 2023-01-27 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_id_liquidacion', '0003_idliquidacion_fecha_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idliquidacion',
            name='fecha_pago',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
