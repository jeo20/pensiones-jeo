# Generated by Django 4.1.5 on 2023-04-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_movimiento_mensual', '0004_movimientomensual_pendiente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientomensual',
            name='modificado',
            field=models.DateTimeField(auto_now=True),
        ),
    ]