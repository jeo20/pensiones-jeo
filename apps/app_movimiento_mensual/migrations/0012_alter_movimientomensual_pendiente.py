# Generated by Django 4.1.5 on 2023-08-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_movimiento_mensual', '0011_alter_movimientomensual_creado_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientomensual',
            name='pendiente',
            field=models.BooleanField(default=True),
        ),
    ]
