# Generated by Django 4.1.5 on 2023-07-31 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_movimiento_mensual', '0007_alter_movimientomensual_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientomensual',
            name='creado_usuario',
            field=models.CharField(default='ADMIN', max_length=30),
        ),
    ]
